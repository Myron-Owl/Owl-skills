# Strict audit, protection and migration

Use only for declared whole-scope protection/audit evidence, linked migration/portable package delivery, strict zero-absolute-path metadata, or custom transactions needing full dependency/protection/recovery contracts. Routine fixed edits keep proportional verification. Unsupported features need scoped native handling, not blanket auditing.

## Prepare, stage and verify

1. Declare authoritative files, upstream-first source order, edit/protection scopes, allowed refresh/execution, expected business results, timeout, save targets and recovery. Prepare the manifest internally; examples are templates, not policy defaults. Inventory relevant package/protection evidence and preserve a coherent recoverable original set with verified hashes.
2. Validate manifest and payload offline. Use scripts/excel-python.cmd for all Python calls. The PowerShell preflight gates custom PowerShell automation only; require PASS_OFFLINE_PREFLIGHT before that custom script starts Excel. Do not run that gate against the existing Python executors.
3. Use existing fixed/batch editors for supported writes; otherwise follow [native transaction guidance](native-edit-transaction.md). Open required sources read-only, upstream first; use task-owned Excel with macros/events disabled unless execution is explicitly authorized. Save only declared targets and never save native-required files through openpyxl.
4. Verify every declared protected scope and acceptance result on staged candidates before final replacement. Routine editors commit after routine checks: run additional strict checks on a disposable candidate copy or within a scoped transaction, then replace the authoritative original only after all checks pass and concurrency/lock checks succeed. Routine success alone does not prove strict whole-scope preservation. Multi-file independent replacement is not atomic commit.
5. Follow [strict validation and recovery](strict-validation.md) for the applicable link/package/protection/report checks. Reopen without repair or saving verification-only changes; verify source-closed behavior when required. Finish when all declared evidence passes.

The manifest modes (automatic/full/full_rebuild) and fixed-editor modes (none/smart/full/rebuild) are separate contracts. Prefer automatic/smart for ordinary result updates; full/rebuild needs a demonstrated reason. Relocation is for actual migration/portable delivery. Strict absolute-path cleanup, macro execution and query refresh require their actual scope/authorization. No automatic screenshot or full package audit merely because formulas exist.

## Establish the Contract

Before editing, create or complete `workbook_manifest.json` from [assets/workbook_manifest.example.json](../assets/workbook_manifest.example.json). Validate it with:

```text
scripts/excel-python.cmd -B scripts/validate_manifest.py workbook_manifest.json
```

For custom PowerShell automation, before starting Microsoft Excel run the deterministic offline gate in `scripts/preflight_excel_payload.ps1` against the automation script, manifest, and compiled write payload when available. On Windows systems that block direct `.ps1` execution, load it explicitly with `Get-Content -Raw -Encoding UTF8` and `ScriptBlock.Create`. Do not start that custom PowerShell native session until the gate returns `PASS_OFFLINE_PREFLIGHT`.

Require explicit values for:

- Entry workbook and complete dependency opening order.
- Editable, expandable, formula-structure-protected, result-protected, and strictly protected ranges.
- Link policy and whether relocation or strict no-absolute-path testing is required.
- Calculation mode, acceptance cells, and business checks.
- Macro policy, save permission, backup path, and timeout.

If a high-risk field is unknown, perform read-only discovery first. Do not infer a writable range or permission to save.

## Protect Existing Content

Classify every relevant cell into one of five scopes:

- `editable`: value, formula, or format may change as declared.
- `expandable`: formulas, validation, conditional formatting, tables, or lookup ranges may extend as declared.
- `formula_structure_protected`: formula text/pattern, formula/constant kind, and declared style evidence must remain equal; cached or displayed results may change through approved upstream recalculation.
- `result_protected`: business result must remain equal; approved formula implementation changes are allowed.
- `strict_protected`: value, formula text, formula/constant kind, blank state, and declared formatting evidence must remain equal.

Compare strict-protected cells individually after the native save. Aggregate totals or a few samples are insufficient.

## Preserve Formula Semantics

- Keep derived results as formulas. Keep assumptions and mapping rules visible and auditable.
- Use stable IDs or explicit mapping tables; do not depend on incidental row order.
- Separate the lookup domain from the current-record domain. For an appendable ID registry, use an Excel Table, dynamic named range, or whole-column lookup when performance is acceptable; do not hard-code the current last row into downstream lookups. Keep business counts and acceptance checks limited to live records identified by stable IDs or status.
- Distinguish true blank, formula `""`, numeric `0`, and lookup failure.
- Do not use a bare reference for an optional field when blank must remain blank; use an explicit blank-preserving formula such as `=IF(Source!A1="","",Source!A1)`.
- Treat A1 formula text, R1C1 pattern, cell kind, cached value, style/number format, and shared-formula metadata as separate evidence.
- Re-read first, boundary, representative middle, and last formulas after Excel saves contiguous formula blocks.
- For programmatically generated formulas, assert expected range tokens and business predicates after write. A syntactically valid shortened range is still a failed edit.
- Validate admissibility rather than equality to a default. A valid explicit override such as `0` must not fail merely because most rows inherit `1`. Test completeness, allowed range, fallback use, and override legality as separate predicates.
- Declare the rounding stage for every multi-layer formula chain. Do not round an intermediate layer unless the workbook contract explicitly requires it; test new or changed logic against zero, negative, blank and relevant boundary inputs before native execution; unchanged input-only edits do not need another formula derivation.
- Never copy an OOXML external-link index such as `[1]` or `[3]` into a new formula. Resolve and write the real workbook name.
- Do not use formula-bar appearance alone as proof that an external link is healthy.

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
