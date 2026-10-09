# Native editing and scoped extensions

Use scripts/edit_native.py for supported fixed-position edits. It uses pywin32, its own Excel instance, read-only sources and a verified staged copy. Do not rewrite this workflow per workbook or run the old PowerShell preflight against the Python executor.

Read this for insertion/deletion/moves, style inheritance, table/rule/name changes, array/spill edits, refresh, signatures or custom multi-file transactions. Fixed edits across files use edit_batch.py and reading-and-recovery.md.

Before building a custom script, check [common operations](common-operations.md). An unsupported local format/rule operation should supply prepare/apply/verify_native methods to edit_native.execute(plan, extension). prepare changes only expected in-memory formats/rules; apply performs those declared native changes; verify_native checks the result before commit. The shared executor owns saving, merged-wrap recovery, reopening, preservation, concurrency checks and replacement. It rejects prepare changes to values, formulas, sheet structure or dimensions. Do not use this local interface for row/column moves, table redesign or arbitrary file writes.

## Bound the extension

Identify affected files/records/ranges/properties and relevant source-to-target dependencies. Prefer existing reserved cells over structural insertion where appropriate. Inserting/moving data requires checking formulas, names, table/validation/conditional-format extents and business boundaries.

Declare spill anchors/extents, check collisions and verify size/results. Legacy arrays require their intended whole array range and correct formula interface. Style inheritance uses an identified same-kind data row and only intended components; never title styles or automatic whole-sheet resizing.

Before opening query/connection workbooks, establish allowed refresh/execution and completion checks. UpdateLinks=0 only controls workbook links. Signatures/encryption require their actual edit consequence/credentials to be resolved; do not remove protection to make a generic script work.

## Native state and performance

Use DispatchEx, never the user's active instance. Disable macros/events before opening target/source files. A blank anchor workbook establishes manual calculation before file opening; set CalculateBeforeSave=false during batching. Track owned objects and close/restore/quit in finally.

Suppress ordinary prompts only for task-owned staged saves after conflict checks, not to decide security matters. Address workbooks/sheets explicitly and use bounded two-dimensional block writes. No save/calculate inside loops. Formula2, Formula and FormulaArray have different semantics.

For permitted local workbook-link calculation, open required sources first and calculate from live cells. This machine can reject redundant UpdateLink calls on open sources. Do not repeat them when declared-source calculation supplies verified results.

## Save and recovery

Use smart calculation first. Full/rebuild requires an identified problem. If a COM method hangs, recover only the task-owned process; do not launch repeated new instances or kill all Excel processes.

Prefer SaveCopyAs beside the original. Ensure temporary manual calculation settings do not become the user's workbook policy: the fixed editor preserves original calcPr metadata in the staged file, then reopens without saving. Never save native/linked workbooks using openpyxl.

For multi-file commits, stage/verify every target and preserve a coherent recovery set; independent file replacements are not an atomic transaction. Keep workbooks closed and stop on concurrent changes.

Apply [validation-and-rollback.md](validation-and-rollback.md) selectively. [manifest-contract.md](manifest-contract.md) is optional for complex scoped transactions. [powershell-com-formula-pitfalls.md](powershell-com-formula-pitfalls.md) applies only to custom PowerShell COM automation.
