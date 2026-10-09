---
name: excel-edit
description: Safely edit existing Excel values, formulas, colors and scoped worksheet extensions while preserving unrelated content. Use lightweight edits for ordinary formula-free XLSX and native Microsoft Excel for formulas, links or VBA. Scale verification to the change; use strict audit for declared whole-scope protection, migration or linked-package delivery.
---

# Edit Excel Workbooks

Edit only requested cells and properties. Choose the engine from file features and the checks from what changes. A complex workbook does not automatically require a full audit.

## Select the verification scope

Choose editing engine and verification scope independently. Formulas, workbook links and VBA require native Excel; their presence alone does not require a full audit.

- **Routine editing (default):** fixed values/formulas/colors and supported formatting, validation, append blocks and new sheets. Use existing executors and checks proportional to affected data/properties/results. No full manifest, package-wide audit, relocation test, screenshot or separate report by default.
- **Strict audit:** declared whole-scope protection/audit evidence, linked-workbook migration or portable package delivery, strict zero-absolute-path metadata, or a custom transaction needing full dependency/protection/recovery contracts. Read [strict-audit.md](references/strict-audit.md). Keep supported writes on the existing editor and verify additional contract evidence on the candidate before authoritative replacement.

Queries, models, ActiveX, signatures, encryption and unsupported structural operations need a scoped native workflow. Resolve actual refresh/execution/preservation requirements; unsupported features do not justify weaker tools or auditing unrelated content. Read only relevant references. Select routes within existing authorization; ask only about real conflicts, missing required information, scope changes or actual permissions.

## Environment

Use [scripts/excel-python.cmd](scripts/excel-python.cmd) for every Python script and package operation in this skill; never bare python, py or pip. Read [references/python-runtime.md](references/python-runtime.md) only for setup/troubleshooting. The current interpreter has openpyxl and pywin32; Codex updates can change its path or packages.

Before preparing the first native edit in a task, run `excel-python.cmd -B check_runtime.py --native` using the absolute script paths. This checks imports without starting Excel. Reuse a successful check within that task; rerun after a runtime/package change or import failure. Missing pywin32 is an environment problem: repair the configured interpreter within authorization, rather than spending time rewriting the editor in PowerShell. Native execution also fails early with structured runtime diagnostics. On this Windows host, use the available application permission escalation for native Excel calls; an 80070520 startup failure needs permission/session diagnosis, not another script language.

## Routine workflow

1. Identify the authoritative file, sheet, records and allowed properties. Resolve the current workspace path internally; a same-named backup on another drive is not the target. Use [read_workbook.py](scripts/read_workbook.py) for bounded summaries/ranges; see [reading and recovery](references/reading-and-recovery.md). Resolve IDs before writing; use exact before-values or additional preconditions to catch stale mappings. Check uniqueness or referenced IDs only if this edit depends on them.
2. For edits, run `read_workbook.py --for-edit` at the first read, before preparing scripts. If replacement is unavailable, notify the user early and continue independent read-only preparation; recheck at commit. Choose the engine using [references/tool-routing.md](references/tool-routing.md). Native engine selection for an authorized edit does not require another user confirmation. Actual filesystem/application permissions still apply.
3. For fixed-position value/formula/color edits, use the tested executor and small [edit plan](references/edit-plan.md). Prefer rectangular operations over per-cell COM calls. Keep this internal JSON in temporary workspace; do not ask the user to author it or present it as an audit manifest.
4. Executors check targets, write a temporary copy beside the original, save once, reopen and verify affected data/styles, and replace the original only after success and a concurrent-change check. Native mode also reopens with sources closed and checks unchanged formulas/link destinations. Failures leave the original in place. An available failed staged copy is retained with bounded differences; inspect it before retrying. It is not a deliverable. After successful completion, remove only this task's diagnosed failure copies.
5. Deliver clickable file names: `[装备表](<F:/actual/path/装备表.xlsx>)`. Put the actual absolute path in the link target only. Do not routinely print absolute paths, cell addresses or before/after lists; provide those only when requested or needed to explain a conflict. Briefly state completion and any material calculation/recovery limitation. Stop when required checks pass. No routine screenshots, PDFs, backup inventory, package audit, hash inventory or separate validation report; provide explicitly required strict-audit evidence.

## Visual checks

Value, formula and color-only edits do not generate screenshots, PDFs or PNGs by default. New sheets or substantial layout changes may justify one visual check of the affected region when actual readability is uncertain. Reuse that preview; repeat only for a concrete remaining visual defect. Prefer a range/screen preview. PDF pagination, fitting to one printed page and print-layout polishing require a printing/PDF requirement; “match the existing appearance” alone does not imply that requirement. If PDF is merely a convenient preview transport, inspect readability without changing print settings or adding pagination requirements. Visual previews never replace formula/style checks.

## Property preservation

- Content edits change only contents. Font-color edits change only that color; fill edits set a solid fill. Preserve font size/name/emphasis, borders, number format, alignment/wrapping, row heights, column widths and merges unless requested.
- Do not auto-fit, redesign, replace a whole font for a color change, or rebuild a sheet. When adding records requires style inheritance, use an identified same-kind data row in a scoped extension, never a title style.
- Conditional formatting can override visible colors. Fixed editors stop on conflicting color targets; inspect the rule before deciding whether to edit static color or the rule. Do not delete rules to force a color.
- Keep leading-zero IDs and literal text beginning with = as strings. Keep blanks, zero, false and formula-empty results distinct. Formula edits use formula operations, not values-only export.
- Filling existing reserved fixed cells is supported. Inserting rows, copying styles or resizing objects is not silently inferred from a content edit.

## Calculation and checks

Small internal-formula files use the same native executor with `dependencies=[]`, `update_links=false`, one session and smart calculation only when results need updating. Do not build a custom transaction merely because internal formulas exist. Read only relevant ranges and load only the needed reference, not every script or legacy checklist. Use the existing fixed editor for inputs/formulas/colors and its optional [append_block](references/edit-plan.md) for supported small additions.

Scale checks to the change: an input-only edit needs requested values, representative dependent results and preservation checks; unchanged formulas do not need another independent model derivation, boundary suite or fill-down exercise. Test new formula logic when introduced; repeat those checks only when that logic changes or evidence warrants it. Compare resolved styles and effective validation behavior, not raw style IDs or XML ordering. `dimension_signature` in edit_common.py supports dimension/style comparisons. Do not introduce another save/reopen or screenshot after the required checks pass.

Color-only edits use no calculation, no source opening and no link refresh. Local property comparisons usually replace screenshots.

Input/formula edits requiring updated results use native smart calculation, the relevant declared source chain and expected business result cells. Formula preservation is not proof of cache freshness. Missing required sources must be reported without claiming successful result validation.

The native executor compares unchanged formulas in memory and checks link targets without per-cell COM formula audits. Full calculation/rebuild needs an identified reason. Relocation tests require a relocation requirement. See [references/validation-and-rollback.md](references/validation-and-rollback.md).

## Scoped extensions

Use optional [format_copies and validations](references/common-operations.md) for selected cell formatting inheritance or whole/decimal/custom single-cell input rules. These run through the same native transaction. For genuinely unsupported local format/rule behavior, use the documented execute(plan, extension) interface rather than rewriting save/check/replace code.

For new worksheets with selected format inheritance, use the native plan's [new_sheets contract](references/new-sheets.md). Combine it with input edits and one existing-sheet append_block for instructions. Do not recreate save/reopen/preservation scripts for supported operations. Read executor source only to debug a demonstrated problem or implement unsupported behavior.

For fixed edits to multiple workbooks, use [edit_batch.py](scripts/edit_batch.py) with the [recovery contract](references/reading-and-recovery.md). It provides guarded recovery for caught failures, not atomic saving. One-file edits retain the normal lightweight workflow.

Insertion/deletion/moves, sorting, table/name/rule changes, spill or legacy-array target edits, query refresh, signatures and encryption require scoped native work. Read [references/native-edit-transaction.md](references/native-edit-transaction.md) and relevant [content guidance](references/workbook-content-and-delivery.md). Do not fall back to openpyxl to evade unsupported features.

The [strict audit workflow](references/strict-audit.md) combines manifest/package-audit/recovery evidence for actual migration, strict-preservation or complex custom transactions. Read [manifest-contract.md](references/manifest-contract.md) only for that purpose and [PowerShell pitfalls](references/powershell-com-formula-pitfalls.md) only when writing custom PowerShell COM code.

Ask only for unresolved conflicts, missing information needed for results, changes in scope, or actual permissions. Reuse authorization already given. Editing does not authorize SVN, downstream export or external sending.

Native formula comparison accepts equivalent worksheet quoting without changing string literals, addresses or operators. New-sheet row heights and widths are checked through Excel after reopening, because package values can use different representations. All native edits can restore the proven loss of wrapping on untouched merged anchors before reopening; unrelated differences still fail. The shared native transaction checks old page settings and validation metadata before replacement; declared validation edits compare effective rules. See [native compatibility](references/native-compatibility.md) only for failures or maintenance.

## Skill maintenance

Use the smallest relevant development test from [maintenance cases](references/maintenance-cases.md). Documentation-only changes do not run Excel. Operation changes run the affected reusable case; changes to saving/repair/commit also run an ordinary native case and the relevant failure checks. Run the full external-link suite only when formula/link/calculation/session or broad transaction changes can affect it. Existing passed tests do not need repeating without a new change or failure. Never run development suites as part of ordinary workbook delivery.

Native timings distinguish execution from planning/diagnosis. Inspect them when investigating slowness, not as a routine user report. Use the skill format validator after metadata changes.
