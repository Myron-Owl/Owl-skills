# Workbook manifest contract

## Purpose

Use one JSON manifest for each dependency set. It declares authority, edit scope, calculation truth, and acceptance criteria before any write occurs. Copy `assets/workbook_manifest.example.json` and replace every placeholder.

## Required fields

- `manifest_version`: schema version used by this skill.
- `excel_target`: target Microsoft Excel edition/version and architecture when known.
- `entry_workbook`: final or primary dependent workbook.
- `dependency_order`: every workbook in source-to-dependent opening order; include the entry workbook.
- `targets`: workbooks permitted to change.
- `ranges`: four scope maps keyed by workbook name.
- `link_policy`: portability and absolute-path rules.
- `calculation`: native calculation and timeout requirements.
- `acceptance`: representative cells, expected values or predicates, error scan, and relocation rules.
- `security`: macro policy and external-content policy.
- `transaction`: dry-run, backup, save, reopen, and rollback requirements.

## Range syntax

Use `Sheet Name!A1:D20`. Quote handling is not needed in JSON range identifiers; the sheet name is everything before the last `!`. Use explicit bounded ranges. Do not use entire rows or columns for protected scopes.

Use `formula_structure_protected` for downstream calculation regions whose formulas must remain identical while values are expected to change after an approved input update. Do not misuse `strict_protected` for those regions.

Each cell or range must have only one strongest effective scope. Resolve overlap by this priority:

```text
strict_protected > formula_structure_protected > result_protected > editable > expandable
```

An editable range overlapping a protected range is a contract error unless a narrower explicit exception is recorded in `notes` and approved by the user.

## Acceptance cells

Each item must include:

- `workbook`
- `sheet`
- `cell`
- `check`: `equals`, `approx`, `one_of`, `not_error`, `formula_equals`, or `custom`
- Expected value/tolerance when applicable
- A short business reason

Representative cells complement, but never replace, whole-scope regression checks.

## Link policies

- `none`: no external workbook links are expected.
- `relative_same_folder`: every source is delivered beside its dependents.
- `relative_tree`: relative subdirectories are allowed and must retain their layout.
- `fixed_absolute`: absolute locations are intentionally required and explicitly approved.

Set `strict_no_absolute_paths` separately. It is stronger than portability and requires a package scan after the final writable Excel save.

## Validation

Run:

```text
python scripts/validate_manifest.py path/to/workbook_manifest.json
```

The validator checks schema shape and common contradictions. It does not prove that ranges exist inside the workbooks or that business expectations are correct.
