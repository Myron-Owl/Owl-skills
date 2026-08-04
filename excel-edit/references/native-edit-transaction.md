# Native edit transaction

## Preflight

Record:

- Absolute paths for formal inputs, temporary workspace, backups, and outputs.
- File hashes, sizes, modified times, lock state, and read-only attributes.
- Microsoft Excel version, calculation mode, automation runtime, and PowerShell/text encoding.
- Dependency direction and opening order.
- Macro policy before the first programmatic open.
- Whether links may update and whether external data refresh is in scope.

For Windows PowerShell scripts containing non-ASCII workbook or sheet names, validate parsing before native execution. Windows PowerShell 5 may decode a UTF-8 file without BOM as the local code page. Prefer a BOM-capable file or load explicitly with `Get-Content -Raw -Encoding UTF8` and `ScriptBlock.Create`. A successful parse check must fail the command on parser errors; do not print a success marker after a non-terminating parser error.

Create a separate Excel application instance. Capture application settings before changing them and restore them in `finally`.

Before requesting a native session, run `../scripts/preflight_excel_payload.ps1`. The offline gate must parse and lint the automation script, validate the manifest, verify compiled block dimensions, check representative generated formulas and boundary math, and serialize both success and failure reports. Native Excel should discover workbook behavior, not basic builder syntax or matrix-count errors.

## Safe application state

For the edit phase, normally set:

- `ScreenUpdating = false`
- `EnableEvents = false`
- `DisplayAlerts` according to the explicit policy; never use it to bypass security decisions
- `Calculation = manual`
- `AutomationSecurity = force-disable` for untrusted or non-macro tasks

Open at least one workbook before changing `Application.Calculation`. Some Excel/COM versions return `0x800A03EC` when calculation mode is set on an otherwise empty application instance. Capture and change calculation mode after the dependency workbooks are open.

Do not assume disabling screen updates suppresses macro security warnings. Set automation security immediately around programmatic opens and restore the previous value afterward.

## Open order

Open upstream sources first and downstream/entry workbooks last. Use explicit link-update arguments. Keep source dependencies read-only unless the manifest lists them as targets.

Do not use active workbook or active sheet as an implicit target. Resolve every workbook, sheet, and range by exact identity.

## Writes

Compile an edit payload before touching Excel. Each operation must declare workbook, sheet, range, write kind, dimensions, and expected old evidence.

Use rectangular two-dimensional arrays for contiguous blocks. Verify that payload dimensions equal target dimensions. Test single-row and multi-row matrix paths independently when using COM/PowerShell.

For dynamic blocks, verify header count, every populated row count, reserved-row count, and the final A1 target range from the same compiled payload. Avoid maintaining a range endpoint separately from the data count when it can be derived.

Separate value blocks from formula blocks where possible. Normalize values crossing the automation boundary to string, Boolean, number, date serial/date, or null as intended.

When generating formulas with PowerShell interpolation, delimit variables adjacent to `:` or letters. For example, use `"D${r}:S${r}"`, not `"D$r:S$r"`; the latter can be interpreted as scoped-variable syntax and silently become a valid but shortened Excel range. Before the full write, test one generated formula and assert its expected literal ranges. After the write, read the formula back from Excel and repeat the assertion at the first, boundary, representative middle, and last rows.

Use the smallest known range for structural operations. Do not call `Cells.UnMerge()` merely to replace a title. Unmerge the exact title range or enumerate known merge areas. Treat data-validation COM calls as fragile: specify the complete operator and required bounds, test one cell first, and use workbook formulas for business validation when interactive validation adds no material value.

Do not calculate or save inside row/cell loops. Finish writes, then calculate once at the required level.

## Calculation

For dependency-sensitive edits:

1. Restore automatic calculation if the workbook contract requires it.
2. Update permitted workbook links.
3. Invoke `CalculateFullRebuild` when formulas, names, dependencies, external links, or calculation versions may have changed.
4. Poll `Application.CalculationState` until `xlDone`.
5. Treat timeout as `FAIL_NATIVE`; do not save a potentially partial calculation.
6. Scan error cells and declared acceptance cells before commit.

`CalculateFullRebuild` applies to all open workbooks and rebuilds dependencies. Keep the application instance isolated so unrelated user workbooks are not included.

## Commit and cleanup

Save only declared targets, normally once. Record saved file hashes. Close the entry workbook, then read-only dependencies. Quit Excel, release automation objects in reverse ownership order, and confirm no target file remains locked.

Restore captured application settings even on failure. Do not terminate unrelated Excel processes.

Suppress meaningless COM return values such as `True` with `[void]` so diagnostic output remains readable. Track a named transaction stage such as `open_workbooks`, `write_sheet`, `calculate`, `save`, or `reopen`; on failure report the stage, workbook, sheet/range, operation, HRESULT/message, and script stack in the same run.

## Reopen

Use a fresh isolated Excel instance for verification. Open formal files read-only. Test with source files closed when the acceptance contract requires closed-source behavior. Do not save verified formal files during this phase.
