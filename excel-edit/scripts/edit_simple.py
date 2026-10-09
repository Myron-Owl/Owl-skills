"""Fixed-location edits for ordinary, formula-free XLSX workbooks."""
from copy import copy
from pathlib import Path
import warnings
from openpyxl.styles import PatternFill
from edit_common import (EditError, require, package_features, check_unlocked, digest, read_book,
                         capture, check_before, cells, stage_path, verify_local, commit, main_cli, effective_style_array)


def execute(p):
    require("append_block" not in p, "Use native editor for append_block")
    require("new_sheets" not in p, "Use native editor for new_sheets")
    require(not p.get("format_copies") and not p.get("validations"), "Use native editor for format inheritance/validation changes")
    original = Path(p["workbook"])
    require(original.suffix.lower() == ".xlsx", "Use native editor for macro workbooks")
    require(p["calculation"] == "none" and not p["dependencies"] and not p["update_links"] and not p["acceptance"], "Simple editor does not calculate or open dependencies")
    require(all(o["kind"] != "formula" for o in p["operations"]), "Use native editor to write formulas")
    check_unlocked(original)
    old_hash = digest(original)
    flags = package_features(original)
    require(not flags, f"Use native/scoped route for workbook features: {sorted(flags)}")
    temp = None
    wb = verified = None
    stage = "preflight"
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error")  # Unsupported-feature warnings must not become silent data loss.
            wb = read_book(original)
            check_before(wb, p)
            baseline = capture(wb, p)
            stage = "write_staged_memory"
            for op in p["operations"]:
                for sh, addr, y, x in cells(op["sheet"], op["range"]):
                    c = wb[sh][addr]
                    if c._style is None:
                        c._style = copy(effective_style_array(c))
                    if op["kind"] == "value":
                        value = op["values"][y][x]
                        c.value = value
                        if isinstance(value, str): c.data_type = "s"
                    elif op["kind"] == "font_color":
                        f = copy(c.font)
                        f.color = "FF"+op["color"][1:].upper()
                        c.font = f
                    else:
                        c.fill = PatternFill(patternType="solid", fgColor="FF"+op["color"][1:].upper())
            stage = "save_copy"
            temp = stage_path(original)
            wb.save(temp)
            wb.close()
            stage = "local_reopen"
            verified = read_book(temp)
            verify_local(verified, p, baseline)
            verified.close()
        stage = "commit"
        saved_hash = digest(temp)
        commit(temp, original, old_hash)
        return {"status": "PASS_LOCAL", "workbook": str(original), "committed_hash": saved_hash, "operations": len(p["operations"]), "recalculated": False}
    except Exception as error:
        raise EditError(str(error), stage=stage, workbook=str(original),
                        failed_file=str(temp if stage == "local_reopen" else original), original_written=False) from error
    finally:
        if wb is not None: wb.close()
        if verified is not None: verified.close()
        if temp is not None and temp.exists(): temp.unlink()


if __name__ == "__main__":
    main_cli(execute, __doc__)
