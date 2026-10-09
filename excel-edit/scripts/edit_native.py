"""Native Excel bounded editor. Original is replaced only after staged native verification."""
from __future__ import annotations

from copy import deepcopy
import gc
import json
import os
import re
from pathlib import Path
import time
import zipfile
from xml.etree import ElementTree as ET

from edit_common import (require, EditError, package_features, check_unlocked, digest, read_book,
                         capture, check_before, cells, bounds, stage_path, verify_local, commit,
                         formula_map, equal, main_cli)


def rgb(color):
    r, g, b = bytes.fromhex(color[1:])
    return r | (g << 8) | (b << 16)


def normalized_links(wb):
    links = wb.LinkSources(1)
    if not links: return []
    if isinstance(links, str): links = [links]
    return sorted(os.path.normcase(os.path.abspath(v)) for v in links)


def get_matrix(rng, prop):
    v = getattr(rng, prop)
    if rng.CountLarge == 1: return [[v]]
    return [list(row) for row in v]


def canonical_matrix(matrix, directory):
    # Tokenize first: never alter quoted string literals or remove apostrophes globally.
    from openpyxl.formula.tokenizer import Tokenizer
    def normalize(value):
        if not isinstance(value, str) or not value.startswith('='): return value
        try: tokens = Tokenizer(value).items
        except Exception: return value  # Unknown syntax remains strictly compared.
        parts = []
        for token in tokens:
            v = token.value
            if token.type == 'OPERAND' and token.subtype == 'RANGE' and '!' in v:
                ref, address = v.rsplit('!', 1)
                if ref.startswith("'") and ref.endswith("'"):
                    ref = ref[1:-1].replace("''", "'")
                m = re.fullmatch(r"(.*)\[([^\]]+)\](.+)", ref)
                if m:
                    folder, book, sheet = m.groups()
                    full = os.path.normcase(os.path.abspath(os.path.join(folder or str(directory), book)))
                    ref = full + '|' + sheet
                # Requote both spellings identically; preserve cell addresses and operators.
                v = "'" + ref.replace("'", "''") + "'!" + address
            parts.append(v)
        return '=' + ''.join(parts)
    return [[normalize(v) for v in row] for row in matrix]


class ExcelSession:
    def __enter__(self):
        import pythoncom
        import win32com.client
        pythoncom.CoInitialize()
        self.app = None
        self.settings = {}
        try:
            # DispatchEx owns a new instance. Never attach to the user's active Excel.
            self.app = win32com.client.DispatchEx("Excel.Application")
            self.app.Visible = False
            for name in ("ScreenUpdating", "EnableEvents", "DisplayAlerts", "AutomationSecurity", "CalculateBeforeSave", "AskToUpdateLinks"):
                self.settings[name] = getattr(self.app, name)
            self.app.ScreenUpdating = False
            self.app.EnableEvents = False
            self.app.AutomationSecurity = 3
            self.app.DisplayAlerts = False
            self.app.AskToUpdateLinks = False
            # A blank workbook establishes manual calculation before opening external files.
            self.anchor = self.app.Workbooks.Add()
            self.settings["Calculation"] = self.app.Calculation
            self.app.Calculation = -4135
            self.app.CalculateBeforeSave = False
            return self
        except Exception:
            self.__exit__(None, None, None)
            raise

    def open(self, path):
        return self.app.Workbooks.Open(str(path), UpdateLinks=0, ReadOnly=True,
                                      IgnoreReadOnlyRecommended=True, Notify=False, AddToMru=False,
                                      Password="", WriteResPassword="", CorruptLoad=0)

    def __exit__(self, exc_type, exc, tb):
        import pythoncom
        cleanup_error = None
        if self.app is not None:
            try:
                # Keep the first, blank anchor while restoring Calculation: Excel rejects
                # this property with no workbooks. All data workbooks close first.
                for i in range(self.app.Workbooks.Count, 1, -1):
                    self.app.Workbooks(i).Close(SaveChanges=False)
                for name, value in self.settings.items():
                    try: setattr(self.app, name, value)
                    except Exception: pass
                if self.app.Workbooks.Count:
                    self.app.Workbooks(1).Close(SaveChanges=False)
            except Exception as e:
                cleanup_error = e
            finally:
                self.anchor = None
                try: self.app.Quit()
                except Exception as e: cleanup_error = cleanup_error or e
                self.anchor = None
                self.app = None
                gc.collect()
        pythoncom.CoUninitialize()
        if cleanup_error is not None and exc is None:
            raise EditError(f"Excel cleanup failed; staged file was not committed: {cleanup_error}")


def preserve_calculation_metadata(original, temp, needs_later_calculation):
    """Manual automation must not leave the user's workbook in manual calculation mode."""
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    with zipfile.ZipFile(original) as src:
        original_xml = ET.fromstring(src.read("xl/workbook.xml"))
        calc = original_xml.find(ns+"calcPr")
        saved_calc = deepcopy(calc) if calc is not None else None
    # Preserve Excel's serialized namespace prefixes by replacing only the calcPr tag.
    import re
    with zipfile.ZipFile(temp) as src:
        entries = [(info, src.read(info.filename)) for info in src.infolist()]
    out = stage_path(temp)
    try:
        with zipfile.ZipFile(out, "w") as dst:
            for info, data in entries:
                if info.filename == "xl/workbook.xml":
                    text = data.decode("utf-8")
                    if saved_calc is None:
                        replacement = ""
                    else:
                        if needs_later_calculation and saved_calc.attrib.get("calcMode", "auto") != "manual":
                            saved_calc.set("fullCalcOnLoad", "1")
                        attrs = " ".join(f'{key}="{value}"' for key, value in saved_calc.attrib.items())
                        replacement = f"<calcPr {attrs}/>"
                    pattern = r"<calcPr\b[^>]*(?:/>|>.*?</calcPr>)"
                    require(re.search(pattern, text) is not None, "Native file has no recognized calcPr; use scoped calculation handling")
                    data = re.sub(pattern, lambda _: replacement, text, count=1, flags=re.S).encode("utf-8")
                dst.writestr(info, data)
        os.replace(out, temp)
    finally:
        if out.exists(): out.unlink()


def verify_results(wb, p):
    for a in p["acceptance"]:
        actual = get_matrix(wb.Worksheets(a["sheet"]).Range(a["range"]), "Value2")
        for y, row in enumerate(a["values"]):
            for x, expected in enumerate(row):
                found = actual[y][x]
                if type(expected) in (int, float) and type(found) in (int, float):
                    ok = abs(expected-found) <= a.get("tolerance", 0)
                else:
                    ok = equal(found, expected)
                require(ok, f"Result mismatch at {a['sheet']}!{a['range']}[{y},{x}]: {found!r}, expected {expected!r}")


class PhaseTimer:
    def __init__(self):
        self.started = self.last = time.perf_counter()
        self.phase = "preflight"
        self.times = {}

    def enter(self, phase):
        now = time.perf_counter()
        self.times[self.phase] = self.times.get(self.phase, 0) + now-self.last
        self.last, self.phase = now, phase
        return phase

    def finish(self):
        self.enter("finished")
        return {k: round(v, 3) for k, v in self.times.items()} | {"total": round(time.perf_counter()-self.started, 3)}


def execute(p, extension=None):
    from check_runtime import require_native
    import append_block
    import new_sheets
    import native_operations
    import native_preservation as preservation
    require_native()
    timing = PhaseTimer()
    original = Path(p["workbook"])
    check_unlocked(original)
    old_hash = digest(original)
    flags = package_features(original)
    unsupported = flags & {"connections", "data_model", "signatures", "xlm_macros", "activex"}
    require(not unsupported, f"Use a scoped native workflow for {sorted(unsupported)}; fixed editor does not manage refresh, signatures or XLM")
    for dep in p["dependencies"]:
        dep_flags = package_features(dep)
        require(not dep_flags.intersection({"connections", "data_model", "signatures", "xlm_macros", "activex"}), f"Dependency needs scoped handling: {dep}")
    dependency_hashes = {d: digest(d) for d in p["dependencies"]}
    wb = read_book(original)  # Inspection only; never save a native workbook through openpyxl.
    try:
        # One transaction for all routes. Extension prepares expected format/rule changes,
        # never saves or changes cell contents/structure during inspection.
        if extension is not None:
            guard = preservation.extension_guard(wb)
            extension.prepare(wb, p)
            require(preservation.extension_guard(wb) == guard, 'Extension changed content or structure during prepare')
        extras = native_operations.prepare(wb, p)
        validation_expected = {s.title:native_operations.validation_map(s) for s in wb} if p.get('validations') else None
        metadata = preservation.capture_metadata(wb)
        if validation_expected is not None:
            for props in metadata.values(): props.pop('data_validations', None)
        protected = preservation.capture_protected(wb, full=bool(extension or p.get('format_copies') or p.get('validations')))
        created = new_sheets.prepare(wb, p)
        check_before(wb, p)
        appended = append_block.prepare(wb, p)
        baseline = capture(wb, p)
        old_formulas = formula_map(wb)
    finally:
        wb.close()
    content_keys = {(sh, addr) for o in p["operations"] if o["kind"] in ("value", "formula") for sh, addr, _, _ in cells(o["sheet"], o["range"])}
    temp = None
    restored_wrap = 0
    succeeded = False
    stage = timing.enter("start_excel")
    active_file = original
    target = deps = check = rng = None
    try:
        with ExcelSession() as session:
            app = session.app
            stage = timing.enter("open_dependency")
            deps = []
            for d in p["dependencies"]:
                active_file = Path(d)
                deps.append(session.open(d))
            stage = timing.enter("open_target")
            active_file = original
            target = session.open(original)
            before_links = normalized_links(target)
            if p["update_links"]:
                available = {os.path.normcase(os.path.abspath(d)) for d in p["dependencies"]}
                require(set(before_links) <= available, "Every refreshed target link must be explicitly listed as a dependency")
                for source in deps:
                    require(set(normalized_links(source)) <= available, "A source has an undeclared upstream link; provide the full relevant dependency chain")
            canonical_formulas = {}
            stage = timing.enter("write")
            new_sheets.apply(target, p.get("new_sheets"))
            append_block.apply(target, p.get("append_block"))
            if extension is not None: extension.apply(target, p)
            native_operations.apply(target, p, extras)
            for op in p["operations"]:
                rng = target.Worksheets(op["sheet"]).Range(op["range"])
                if op["kind"] in ("value", "formula"):
                    require(rng.HasArray is False, "Legacy array formula target needs a scoped edit")
                    require(rng.HasSpill is False, "Spill formula target needs a scoped edit")
                    require(not rng.MergeCells or rng.CountLarge == 1, "Use only the merged anchor for content edits")
                    if op["kind"] == "formula":
                        # Excel may inherit percentage/date formatting from a referenced cell.
                        number_format = rng.NumberFormat
                        formats = None if number_format is not None else [
                            (rng.Cells(y+1,x+1), rng.Cells(y+1,x+1).NumberFormat)
                            for y,row in enumerate(op['values']) for x in range(len(row))]
                        rng.Formula2 = tuple(tuple(row) for row in op["values"])
                        if formats is None:
                            rng.NumberFormat = number_format
                        else:
                            for cell, fmt in formats: cell.NumberFormat = fmt
                            cell = formats = None
                        require(rng.HasSpill is False, "New spilling formula needs a declared spill area and scoped validation")
                        actual = get_matrix(rng, "Formula2")
                        actual = canonical_matrix(actual, original.parent)
                        require(actual == canonical_matrix(op["values"], original.parent), f"Formula mismatch at {op['sheet']}!{op['range']}: expected {op['values']!r}, actual {actual!r}")
                        canonical_formulas[(op["sheet"], op["range"])] = actual
                    else:
                        # Prefix text for Excel to preserve leading zeroes and literal formula-like text.
                        values = tuple(tuple("'"+v if isinstance(v, str) else v for v in row) for row in op["values"])
                        rng.Value2 = values
                        require(get_matrix(rng, "Value2") == op["values"], "Excel changed input types; source kept")
                elif op["kind"] == "font_color":
                    rng.Font.Color = rgb(op["color"])
                else:
                    rng.Interior.Pattern = 1
                    rng.Interior.Color = rgb(op["color"])
            # Writing wrapped text may auto-fit a new row. Reapply only declared new heights.
            for spec in p.get("new_sheets", []):
                if "row_height" in spec:
                    _, first, _, last = bounds(spec["range"])
                    target.Worksheets(spec["name"]).Rows(f"{first}:{last}").RowHeight = spec["row_height"]
            stage = timing.enter("calculate")
            expected_links = sorted(os.path.normcase(os.path.abspath(v)) for v in p.get("expected_links", before_links))
            require(normalized_links(target) == expected_links, "Unexpected external link targets; declare expected_links for an intentional link edit")
            if p["update_links"]:
                require(set(expected_links) <= available, "New calculated link source is missing from dependencies")
            # All declared sources are already open. Calculation reads their live cells;
            # UpdateLink is redundant and fails on some Excel builds for open sources.
            if p["calculation"] != "none":
                start = time.monotonic()
                {"smart": app.Calculate, "full": app.CalculateFull, "rebuild": app.CalculateFullRebuild}[p["calculation"]]()
                while app.CalculationState != 0:
                    require(time.monotonic()-start < p["timeout_seconds"], "Calculation timeout; source kept")
                    time.sleep(0.1)
            verify_results(target, p)
            require(normalized_links(target) == expected_links, "Unexpected external link targets; declare expected_links for an intentional link edit")
            stage = timing.enter("save_copy")
            temp = stage_path(original)
            target.SaveCopyAs(str(temp))
            target.Close(SaveChanges=False)
            target = rng = None
            for dep in reversed(deps): dep.Close(SaveChanges=False)
            deps = None
            preserve_calculation_metadata(original, temp, bool(content_keys) and p["calculation"] == "none")
            restored_wrap = preservation.restore_merged_wrap(temp, protected, p)
            stage = timing.enter("native_reopen")
            active_file = temp
            check = session.open(temp)  # Source workbooks are closed; no update and no repair request.
            new_sheets.verify_native(check, p.get('new_sheets'))
            if extension is not None: extension.verify_native(check, p)
            require(normalized_links(check) == expected_links, "Saved external link targets changed")
            for (sheet, address), expected in canonical_formulas.items():
                require(canonical_matrix(get_matrix(check.Worksheets(sheet).Range(address), "Formula2"), original.parent) == expected, f"Saved formula changed at {sheet}!{address}")
            verify_results(check, p)
            check.Close(SaveChanges=False)
            check = app = None
            stage = timing.enter("close_excel")
        stage = timing.enter("local_preservation")
        saved = read_book(temp)
        try:
            verify_local(saved, p, baseline, native=True)
            append_block.verify(saved, p, appended)
            new_sheets.verify(saved, p, created, native=True)
            preservation.verify_metadata(saved, metadata)
            preservation.verify_protected(saved, protected, p)
            if validation_expected is not None:
                require({s: native_operations.validation_map(saved[s]) for s in validation_expected} == validation_expected,
                        'Validation behavior differs outside or inside declared edits')
            saved_formulas = formula_map(saved)
            require({k: v for k, v in old_formulas.items() if k not in content_keys} ==
                    {k: v for k, v in saved_formulas.items() if k not in content_keys},
                    "An unrequested formula changed; original kept")
        finally:
            saved.close()
        require(all(digest(d) == h for d, h in dependency_hashes.items()), "A dependency changed during the edit; original target kept")
        stage = timing.enter("commit")
        active_file = original
        saved_hash = digest(temp)
        commit(temp, original, old_hash)
        succeeded = True
        return {"restored_merged_wrap": restored_wrap, "status": "PASS_NATIVE_LOCAL", "workbook": str(original), "committed_hash": saved_hash, "operations": len(p["operations"]),
                "recalculated": p["calculation"] != "none", "links_updated": p["update_links"], "source_closed_reopen": True, "timings_seconds": timing.finish()}
    except Exception as e:
        diagnostics = preservation.diagnose(temp, p, baseline, protected) if temp is not None and temp.exists() else []
        raise EditError(f"{stage}: {e}", stage=stage, workbook=str(original),
                        diagnostic_differences=diagnostics, staged_file=str(temp) if temp is not None and temp.exists() else None,
                        failed_file=str(active_file), original_written=False, timings_seconds=timing.finish()) from e
    finally:
        target = deps = check = rng = None
        gc.collect()
        if succeeded and temp is not None and temp.exists(): temp.unlink()


if __name__ == "__main__":
    main_cli(execute, __doc__)
