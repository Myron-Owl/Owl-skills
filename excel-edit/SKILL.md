---
name: excel-edit
description: Safely inspect, create, edit, recalculate, validate, and deliver Microsoft Excel workbooks, especially existing .xlsx/.xlsm files with dense formula chains, cross-sheet formulas, cross-workbook links, named ranges, shared or dynamic formulas, macros, data connections, or strict preservation requirements. Use for Excel changes that require native Microsoft Excel truth, minimal targeted edits, dependency-aware opening, formula/link regression checks, OOXML package auditing, rollback, relocation testing, or a machine-readable workbook manifest. Do not use for game-design balancing or project-specific numeric design rules.
---

# Edit Excel Workbooks

Treat an Excel edit as a transaction over a dependency graph, not as a cell-writing task. Preserve the original file, make the smallest authorized change, and use Microsoft Excel as the calculation oracle whenever workbook behavior matters.

## Route Before Acting

Read [references/tool-routing.md](references/tool-routing.md), classify the task, and record the selected route in the edit plan.

Use native Microsoft Excel editing when any condition applies:

- The workbook contains cross-workbook formulas, macros, Power Query, Power Pivot, a data model, external connections, shared formulas, dynamic arrays, or modern functions whose serialization may be tool-specific.
- The task must preserve cached values, external-link relationships, calculation behavior, or Excel-native results.
- The user requires exact compatibility with Microsoft Excel, strict protected ranges, or a portable multi-workbook package.

Use a standalone workbook library only for low-risk new workbooks or explicitly accepted structure-only operations. Never silently downgrade a native-required task. If native validation is unavailable, return `PASS_STRUCTURE_ONLY` at best, never `PASS_NATIVE`.

## Load Only Needed References

- For every edit, read [references/manifest-contract.md](references/manifest-contract.md).
- For native or linked-workbook edits, read [references/native-edit-transaction.md](references/native-edit-transaction.md).
- For delivery, strict protection, external links, or recovery, read [references/validation-and-rollback.md](references/validation-and-rollback.md).
- For provenance or disputed technical behavior, read [references/technical-sources.md](references/technical-sources.md).

## Establish the Contract

Before editing, create or complete `workbook_manifest.json` from [assets/workbook_manifest.example.json](assets/workbook_manifest.example.json). Validate it with:

```text
python scripts/validate_manifest.py workbook_manifest.json
```

Require explicit values for:

- Entry workbook and complete dependency opening order.
- Editable, expandable, formula-structure-protected, result-protected, and strictly protected ranges.
- Link policy and whether relocation or strict no-absolute-path testing is required.
- Calculation mode, acceptance cells, and business checks.
- Macro policy, save permission, backup path, and timeout.

If a high-risk field is unknown, perform read-only discovery first. Do not infer a writable range or permission to save.

## Execute the Transaction

Use this fixed sequence:

1. **Preflight** — confirm files, locks, target Excel version, runtime paths, encoding, permissions, macro policy, dependency order, and available disk space.
2. **Inventory** — capture sheets, names, tables, formulas, links, protected-range baselines, file hashes, and package structure. Run `scripts/inspect_xlsx_package.py` for `.xlsx` or `.xlsm` inputs.
3. **Dry run** — compile the user request into [assets/edit_plan.example.json](assets/edit_plan.example.json). List every intended write and every range that must not change.
4. **Backup** — create recoverable copies outside the formal delivery set and verify their hashes.
5. **Native session** — start an isolated Microsoft Excel instance; do not attach to the user's unrelated interactive instance. Set macro security before programmatic opens.
6. **Open dependencies** — open source workbooks before dependent workbooks, using the manifest order. Keep non-target dependencies read-only unless explicitly writable.
7. **Edit** — disable events, screen updating, and automatic calculation temporarily. Write contiguous value and formula blocks as correctly sized two-dimensional matrices. Keep values and formulas in separate writes when practical. Avoid repeated saves and recalculations.
8. **Recalculate** — update permitted links, call full dependency rebuild when required, wait until calculation state is done, then scan errors and acceptance cells.
9. **Commit** — save only authorized target workbooks, normally once. Close all workbooks, quit the isolated Excel instance, release automation objects, and confirm locks are gone.
10. **Reopen verification** — reopen the formal files read-only, with source files closed where the contract requires it. Recheck formulas, links, acceptance results, and protected ranges. Do not save during this phase.
11. **Relocation/package verification** — when required, copy the entire dependency set to a different directory and repeat read-only verification. Audit the OOXML package after the last writable save.
12. **Report or rollback** — emit [assets/validation_report.example.json](assets/validation_report.example.json). On failure, follow the rollback order exactly.

## Preserve Formula Semantics

- Keep derived results as formulas. Keep assumptions and mapping rules visible and auditable.
- Use stable IDs or explicit mapping tables; do not depend on incidental row order.
- Distinguish true blank, formula `""`, numeric `0`, and lookup failure.
- Treat A1 formula text, R1C1 pattern, cell kind, cached value, style/number format, and shared-formula metadata as separate evidence.
- Re-read first, boundary, representative middle, and last formulas after Excel saves contiguous formula blocks.
- Never copy an OOXML external-link index such as `[1]` or `[3]` into a new formula. Resolve and write the real workbook name.
- Do not use formula-bar appearance alone as proof that an external link is healthy.

## Protect Existing Content

Classify every relevant cell into one of four scopes:

- `editable`: value, formula, or format may change as declared.
- `expandable`: formulas, validation, conditional formatting, tables, or lookup ranges may extend as declared.
- `formula_structure_protected`: formula text/pattern, formula/constant kind, and declared style evidence must remain equal; cached or displayed results may change through approved upstream recalculation.
- `result_protected`: business result must remain equal; approved formula implementation changes are allowed.
- `strict_protected`: value, formula text, formula/constant kind, blank state, and declared formatting evidence must remain equal.

Compare strict-protected cells individually after the native save. Aggregate totals or a few samples are insufficient.

## Fail Safely

Use these terminal states:

- `PASS_NATIVE` — native edit, full required calculation, reopen, protection, link, and relocation checks passed.
- `PASS_STRUCTURE_ONLY` — package and formula-text checks passed, but native truth was unavailable.
- `WARNING_TOOL_LIMITATION` — a tool could not evaluate a feature; no success claim is implied.
- `FAIL_BUSINESS` — formulas or results violate the declared business checks.
- `FAIL_STRUCTURE` — package, relationship, range, or serialization checks failed.
- `FAIL_NATIVE` — Microsoft Excel repaired, rejected, miscalculated, timed out, or failed reopening the workbook.
- `ROLLED_BACK` — formal files were restored and their backup hashes verified.

Never leave a half-completed workbook in the formal delivery directory. Never overwrite a locked workbook during rollback.

## Completion Gate

Finish only when all required evidence exists:

- Intended writes match the dry-run plan.
- Unmodified and protected scopes pass their declared comparison level.
- Formula error scan is clean or every allowed exception is listed.
- External links resolve under the declared source-closed and relocation conditions.
- Microsoft Excel completes calculation before timeout, saves without repair, closes, and reopens cleanly when native validation is required.
- Visual inspection covers all affected user-facing sheets.
- The report states the exact validation tier and known limitations.
