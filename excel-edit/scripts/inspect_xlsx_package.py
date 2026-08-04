#!/usr/bin/env python3
"""Read-only structural inventory for .xlsx/.xlsm OOXML packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
DOC_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
ABS_PATTERNS = (
    re.compile(r"(?i)(?:^|[^A-Za-z])[A-Z]:[\\/]"),
    re.compile(r"(?i)file:///?"),
    re.compile(r"^\\\\"),
)
ABS_TEXT_RE = re.compile(
    r"(?i)(?:file:///[A-Z]:[\\/][^<\"']+|(?<![A-Za-z0-9])[A-Z]:[\\/][^<\"']+|\\\\[^<\"']+)"
)


def is_absolute_target(value: str) -> bool:
    return any(pattern.search(value) for pattern in ABS_PATTERNS)


def parse_xml(zf: zipfile.ZipFile, name: str):
    try:
        return ET.fromstring(zf.read(name))
    except KeyError:
        return None


def rels(zf: zipfile.ZipFile, name: str) -> list[dict]:
    root = parse_xml(zf, name)
    if root is None:
        return []
    items = []
    for node in root.findall(f"{{{REL_NS}}}Relationship"):
        items.append(
            {
                "id": node.attrib.get("Id"),
                "type": node.attrib.get("Type"),
                "target": node.attrib.get("Target"),
                "target_mode": node.attrib.get("TargetMode"),
            }
        )
    return items


def workbook_sheets(zf: zipfile.ZipFile) -> list[dict]:
    root = parse_xml(zf, "xl/workbook.xml")
    if root is None:
        return []
    sheets = []
    for node in root.findall(f".//{{{MAIN_NS}}}sheet"):
        sheets.append(
            {
                "name": node.attrib.get("name"),
                "sheet_id": node.attrib.get("sheetId"),
                "relationship_id": node.attrib.get(f"{{{DOC_REL_NS}}}id"),
                "state": node.attrib.get("state", "visible"),
            }
        )
    return sheets


def workbook_names(zf: zipfile.ZipFile) -> list[dict]:
    root = parse_xml(zf, "xl/workbook.xml")
    if root is None:
        return []
    names = []
    for node in root.findall(f".//{{{MAIN_NS}}}definedName"):
        names.append(
            {
                "name": node.attrib.get("name"),
                "local_sheet_id": node.attrib.get("localSheetId"),
                "hidden": node.attrib.get("hidden"),
                "refers_to": node.text or "",
            }
        )
    return names


def formula_inventory(zf: zipfile.ZipFile, sample_limit: int) -> dict:
    worksheet_names = sorted(
        name
        for name in zf.namelist()
        if re.fullmatch(r"xl/worksheets/sheet[0-9]+\.xml", name)
    )
    total = 0
    shared = 0
    array = 0
    dynamic = 0
    external_formula_samples = []
    error_literal_hits = []
    for name in worksheet_names:
        root = parse_xml(zf, name)
        if root is None:
            continue
        for cell in root.findall(f".//{{{MAIN_NS}}}c"):
            address = cell.attrib.get("r")
            formula = cell.find(f"{{{MAIN_NS}}}f")
            value = cell.find(f"{{{MAIN_NS}}}v")
            if formula is not None:
                total += 1
                formula_type = formula.attrib.get("t")
                shared += formula_type == "shared"
                array += formula_type == "array"
                text = formula.text or ""
                if "[" in text and len(external_formula_samples) < sample_limit:
                    external_formula_samples.append({"part": name, "cell": address, "formula": text})
                if any(token in text for token in ("_xlfn.", "_xlpm.")):
                    dynamic += 1
            if value is not None and value.text in {"#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A"}:
                error_literal_hits.append({"part": name, "cell": address, "value": value.text})
    return {
        "worksheet_parts": len(worksheet_names),
        "formula_count": total,
        "shared_formula_cells": shared,
        "array_formula_cells": array,
        "modern_formula_prefix_cells": dynamic,
        "external_formula_samples": external_formula_samples,
        "cached_error_literals": error_literal_hits,
    }


def inspect(path: Path, formula_sample_limit: int) -> dict:
    result = {
        "path": str(path.resolve()),
        "is_zip": zipfile.is_zipfile(path),
        "package_parts": 0,
        "sheets": [],
        "defined_names": [],
        "workbook_relationships": [],
        "external_link_relationships": [],
        "external_link_parts": [],
        "absolute_path_hits": [],
        "formulas": {},
        "warnings": [],
    }
    if not result["is_zip"]:
        result["warnings"].append("not an OOXML zip package")
        return result

    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        result["package_parts"] = len(names)
        result["sheets"] = workbook_sheets(zf)
        result["defined_names"] = workbook_names(zf)
        result["workbook_relationships"] = rels(zf, "xl/_rels/workbook.xml.rels")
        result["external_link_parts"] = sorted(
            name for name in names if name.startswith("xl/externalLinks/")
        )
        result["formulas"] = formula_inventory(zf, formula_sample_limit)

        for name in result["external_link_parts"]:
            if not name.endswith(".rels"):
                continue
            for item in rels(zf, name):
                result["external_link_relationships"].append({"part": name, **item})

        absolute_hits = set()
        for name in names:
            if not (name.endswith(".xml") or name.endswith(".rels")):
                continue
            try:
                text = zf.read(name).decode("utf-8", errors="replace")
            except KeyError:
                continue
            for match in ABS_TEXT_RE.finditer(text):
                value = match.group(0)
                if is_absolute_target(value):
                    absolute_hits.add((name, value[:500]))
        result["absolute_path_hits"] = [
            {"part": name, "text": value} for name, value in sorted(absolute_hits)
        ]

        relationship_targets = [
            item.get("target") or "" for item in result["workbook_relationships"]
        ]
        if result["formulas"].get("external_formula_samples") and not result["external_link_parts"]:
            result["warnings"].append("external-looking formulas exist but no externalLinks parts were found")
        if any(is_absolute_target(target) for target in relationship_targets):
            result["warnings"].append("absolute workbook relationship target found")

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--formula-sample-limit", type=int, default=12)
    args = parser.parse_args()
    if not args.workbook.is_file():
        print(json.dumps({"error": "workbook not found", "path": str(args.workbook)}, ensure_ascii=False))
        return 2
    if args.formula_sample_limit < 0:
        parser.error("--formula-sample-limit must be non-negative")
    report = inspect(args.workbook, args.formula_sample_limit)
    print(json.dumps(report, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0 if report["is_zip"] else 1


if __name__ == "__main__":
    sys.exit(main())
