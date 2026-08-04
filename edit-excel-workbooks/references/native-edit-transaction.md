# Native edit transaction

## Preflight

Record:

- Absolute paths for formal inputs, temporary workspace, backups, and outputs.
- File hashes, sizes, modified times, lock state, and read-only attributes.
- Microsoft Excel version, calculation mode, automation runtime, and PowerShell/text encoding.
- Dependency direction and opening order.
- Macro policy before the first programmatic open.
- Whether links may update and whether external data refresh is in scope.

Create a separate Excel application instance. Capture application settings before changing them and restore them in `finally`.

## Safe application state

For the edit phase, normally set:

- `ScreenUpdating = false`
- `EnableEvents = false`
- `DisplayAlerts` according to the explicit policy; never use it to bypass security decisions
- `Calculation = manual`
- `AutomationSecurity = force-disable` for untrusted or non-macro tasks

Do not assume disabling screen updates suppresses macro security warnings. Set automation security immediately around programmatic opens and restore the previous value afterward.

## Open order

Open upstream sources first and downstream/entry workbooks last. Use explicit link-update arguments. Keep source dependencies read-only unless the manifest lists them as targets.

Do not use active workbook or active sheet as an implicit target. Resolve every workbook, sheet, and range by exact identity.

## Writes

Compile an edit payload before touching Excel. Each operation must declare workbook, sheet, range, write kind, dimensions, and expected old evidence.

Use rectangular two-dimensional arrays for contiguous blocks. Verify that payload dimensions equal target dimensions. Test single-row and multi-row matrix paths independently when using COM/PowerShell.

Separate value blocks from formula blocks where possible. Normalize values crossing the automation boundary to string, Boolean, number, date serial/date, or null as intended.

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

## Reopen

Use a fresh isolated Excel instance for verification. Open formal files read-only. Test with source files closed when the acceptance contract requires closed-source behavior. Do not save verified formal files during this phase.

