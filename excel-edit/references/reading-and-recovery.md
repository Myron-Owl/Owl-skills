# Reading, diagnosis and multi-file recovery

Use the fixed launcher with `scripts/read_workbook.py WORKBOOK` for a sheet/table summary. Add `--sheet NAME --range A1:H12` for a bounded read (maximum 1,000 cells). Add `--cached` only when stored formula results are useful; this does not calculate or establish freshness. No workbook is saved. Avoid long inline Python through PowerShell and unbounded formula dumps.

Rich text is converted to visible text only for matching and reporting. Stored rich text remains intact for unrelated/color-only edits. A requested full value replacement replaces its contents, including rich text runs. Interpret business units from headers/formulas: a multiplier delta of +100% may be numeric 1, not 100; do not change number formats unless requested.

Both editors inspect existing Excel Table headers before writing and after staged saving. A visible header differing from its internal tableColumn name can prevent native Excel from opening even when ZIP/XML parsing succeeds. This is a diagnostic lead, not proof that every open error has this cause. Ordinary ranges without Excel Tables have no such metadata check. Fixed editors refuse table header content changes because structured references may also need renaming.

For mismatches, inspect an isolated copy. Before proposing column-name synchronization, examine affected structured references, defined names and declared dependent workbooks; do not blindly rename metadata or globally replace strings. If dependencies are unavailable, state that repair safety is unresolved. For an authorized repair, change only the demonstrated defective metadata, compare changed ZIP parts for that repair, and prove normal native opening on the copy before committing. Do not enable repair mode or strip workbook features as an automatic workaround.

Native failures identify stage, failed_file and original_written. When a staged file exists, staged_file identifies a retained diagnostic copy and diagnostic_differences provides bounded before/after properties. Inspect this copy instead of rerunning merely to gather evidence; never deliver it as the completed workbook. After a successful retry remove only this task's diagnosed failure copies. If the task remains unresolved, retain them for diagnosis. Distinguish opening a dependency, opening the target, saving the staged copy, reopening it and committing. After an unchanged failure, diagnose the stated stage instead of repeatedly reopening/recalculating. COM timeout_seconds bounds calculation-state polling only; it cannot interrupt a blocking Excel COM call. Do not kill the user's Excel instance.

## Multiple edited workbooks

Only when two or more files are actually edited, call `scripts/edit_batch.py BATCH_JSON`. The internal JSON has exactly these fields:

```json
{
  "steps": [
    {"engine": "native", "plan": "F:/temporary/source-plan.json"},
    {"engine": "native", "plan": "F:/temporary/dependent-plan.json"}
  ],
  "recovery_directory": "F:/temporary/new-unique-recovery-folder"
}
```

Each plan uses the existing edit-plan contract. Use absolute paths and a new recovery directory outside delivered material. Targets occur once, with upstream targets first. Cyclic dependencies need scoped handling. A source that is merely read is a dependency, not another edited target.

The wrapper validates plans, backs up the edited originals, records a small recovery journal, then runs the standard editors sequentially. On a caught failure it restores earlier committed files only if their current hashes still match the bytes written by this task and the backups remain intact. Concurrent or uncertain changes block that file's restoration; preserve the journal/backups and explain the partial state. Do not automatically retry the batch with stale before-values.

This is recoverable sequential saving, not an atomic transaction across files. Process termination/power failure or interrupted journaling can require manual recovery. Keep backups through verification and until recovery is no longer needed; do not delete them during an unresolved failure. Ordinary one-file edits do not use this wrapper or create this backup inventory. The journal and hashes stay internal and are not routine user-facing deliverables.
