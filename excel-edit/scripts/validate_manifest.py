#!/usr/bin/env python3
"""Validate the operational shape of an excel-edit manifest."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


RANGE_RE = re.compile(r"^.+![A-Z]{1,3}[1-9][0-9]*(?::[A-Z]{1,3}[1-9][0-9]*)?$")
SCOPES = (
    "editable",
    "expandable",
    "formula_structure_protected",
    "result_protected",
    "strict_protected",
)
LINK_MODES = {"none", "relative_same_folder", "relative_tree", "fixed_absolute"}
CALC_MODES = {"automatic", "full", "full_rebuild"}
MACRO_POLICIES = {"force_disable", "by_ui", "allow_signed", "explicit_user_run"}
CELL_CHECKS = {"equals", "approx", "one_of", "not_error", "formula_equals", "custom"}


def require(mapping: dict, key: str, kind: type, errors: list[str], path: str = ""):
    label = f"{path}.{key}" if path else key
    if key not in mapping:
        errors.append(f"missing required field: {label}")
        return None
    value = mapping[key]
    if not isinstance(value, kind):
        errors.append(f"{label} must be {kind.__name__}")
        return None
    return value


def nonempty_strings(values, label: str, errors: list[str]) -> list[str]:
    if not isinstance(values, list) or not values:
        errors.append(f"{label} must be a non-empty array")
        return []
    result = []
    for index, value in enumerate(values):
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{label}[{index}] must be a non-empty string")
        else:
            result.append(value)
    if len(result) != len(set(result)):
        errors.append(f"{label} contains duplicates")
    return result


def validate(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest root must be an object"]

    require(data, "manifest_version", str, errors)
    require(data, "excel_target", dict, errors)
    entry = require(data, "entry_workbook", str, errors)
    order = nonempty_strings(data.get("dependency_order"), "dependency_order", errors)
    targets = nonempty_strings(data.get("targets"), "targets", errors)

    if entry and order and entry not in order:
        errors.append("entry_workbook must appear in dependency_order")
    unknown_targets = sorted(set(targets) - set(order))
    if unknown_targets:
        errors.append(f"targets absent from dependency_order: {unknown_targets}")

    ranges = require(data, "ranges", dict, errors)
    if ranges is not None:
        declared_ranges: dict[tuple[str, str], str] = {}
        for scope in SCOPES:
            mapping = require(ranges, scope, dict, errors, "ranges")
            if mapping is None:
                continue
            for workbook, identifiers in mapping.items():
                if workbook not in order:
                    errors.append(f"ranges.{scope} names unknown workbook: {workbook}")
                if scope in {"editable", "expandable"} and workbook not in targets:
                    errors.append(f"ranges.{scope} names non-target workbook: {workbook}")
                if not isinstance(identifiers, list):
                    errors.append(f"ranges.{scope}.{workbook} must be an array")
                    continue
                for index, identifier in enumerate(identifiers):
                    if not isinstance(identifier, str) or not RANGE_RE.match(identifier):
                        errors.append(
                            f"ranges.{scope}.{workbook}[{index}] must use Sheet!A1 or Sheet!A1:B2"
                        )
                    elif (workbook, identifier) in declared_ranges:
                        errors.append(
                            f"range {workbook}|{identifier} appears in both "
                            f"{declared_ranges[(workbook, identifier)]} and {scope}"
                        )
                    else:
                        declared_ranges[(workbook, identifier)] = scope

    link_policy = require(data, "link_policy", dict, errors)
    if link_policy is not None:
        mode = require(link_policy, "mode", str, errors, "link_policy")
        if mode and mode not in LINK_MODES:
            errors.append(f"link_policy.mode must be one of {sorted(LINK_MODES)}")
        require(link_policy, "strict_no_absolute_paths", bool, errors, "link_policy")
        allowed = link_policy.get("allowed_external_workbooks", [])
        if not isinstance(allowed, list) or any(not isinstance(x, str) for x in allowed):
            errors.append("link_policy.allowed_external_workbooks must be an array of strings")
        elif sorted(set(allowed) - set(order)):
            errors.append(
                "link_policy.allowed_external_workbooks absent from dependency_order: "
                f"{sorted(set(allowed) - set(order))}"
            )
        if mode == "none" and allowed:
            errors.append("link_policy.mode=none conflicts with allowed_external_workbooks")

    calculation = require(data, "calculation", dict, errors)
    if calculation is not None:
        mode = require(calculation, "mode", str, errors, "calculation")
        if mode and mode not in CALC_MODES:
            errors.append(f"calculation.mode must be one of {sorted(CALC_MODES)}")
        timeout = require(calculation, "timeout_seconds", int, errors, "calculation")
        if timeout is not None and timeout <= 0:
            errors.append("calculation.timeout_seconds must be positive")
        require(calculation, "wait_for_done", bool, errors, "calculation")
        require(calculation, "update_workbook_links", bool, errors, "calculation")

    acceptance = require(data, "acceptance", dict, errors)
    if acceptance is not None:
        require(acceptance, "scan_formula_errors", bool, errors, "acceptance")
        require(acceptance, "reopen_read_only", bool, errors, "acceptance")
        require(acceptance, "relocation_test", bool, errors, "acceptance")
        cells = require(acceptance, "cells", list, errors, "acceptance")
        if cells is not None:
            for index, cell in enumerate(cells):
                label = f"acceptance.cells[{index}]"
                if not isinstance(cell, dict):
                    errors.append(f"{label} must be an object")
                    continue
                for key in ("workbook", "sheet", "cell", "check", "reason"):
                    require(cell, key, str, errors, label)
                if cell.get("workbook") not in order:
                    errors.append(f"{label}.workbook is absent from dependency_order")
                if cell.get("check") not in CELL_CHECKS:
                    errors.append(f"{label}.check must be one of {sorted(CELL_CHECKS)}")

    security = require(data, "security", dict, errors)
    if security is not None:
        policy = require(security, "macro_policy", str, errors, "security")
        if policy and policy not in MACRO_POLICIES:
            errors.append(f"security.macro_policy must be one of {sorted(MACRO_POLICIES)}")

    transaction = require(data, "transaction", dict, errors)
    if transaction is not None:
        for key in (
            "require_dry_run",
            "require_backup",
            "allow_save",
            "save_targets_only",
            "rollback_on_failure",
        ):
            require(transaction, key, bool, errors, "transaction")
        sessions = require(transaction, "max_writable_sessions", int, errors, "transaction")
        if sessions is not None and sessions != 1:
            errors.append("transaction.max_writable_sessions must be 1 for this skill")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        return 2

    errors = validate(data)
    print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
