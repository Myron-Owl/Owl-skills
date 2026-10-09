# Checks proportional to changes

## Routine minimum

Check target identity and before-values, save once to a staged file, reopen it, verify written types/values/colors and preserve unrequested local style properties and dimensions. Commit only after success and a concurrent-change check. Library reopening is not Excel calculation proof.

Native editing additionally checks unchanged formulas/link targets and reopens with source workbooks closed, link updates disabled and normal load (no repair/extraction). Do not add repeated reopening, PDF export or reports after these pass without new evidence.

| Trigger | Additional check |
|---|---|
| Inputs/formulas needing updated results | Required source chain, smart calculation and explicit expected business results |
| Repeated/generated formula blocks | First/last and mapping boundaries in generation; executor checks requested formula blocks |
| Insertion/deletion/movement/object expansion | Affected formulas/names/tables/validation/conditional-format ranges and active-ID counts |
| New external reference | Intended source/sheet/range, expected link list, business result, source-closed reopen |
| Moving/renaming linked delivery files | Requested directory-layout relocation test |
| Strict zero absolute metadata | Targeted package audit after final native save |
| Actual layout/readability/color ambiguity | Inspect affected range visually; screenshot only when needed |
| Queries/macros/specialized features | Their specific allowed refresh/execution/preservation behavior |

If error scans are useful, compare before/after in affected result regions, include relevant #SPILL!/#CALC! errors, and distinguish old errors from introduced errors. Do not repair unrelated old errors. No-error results can still use wrong ranges: check expected values/counts. Full/rebuild calculation requires an identified issue.

## Recovery

Fixed editors retain the original until staged verification succeeds, then replace it in the same directory. On failure close the owned Excel instance without saving originals. Retain available failed staging copies for bounded diagnostics and inspect before retrying; remove only diagnosed task-owned copies after successful recovery, within authorization. Never overwrite a locked source or claim successful recovery when cleanup failed.

For custom operations without staged replacement, retain a recovery copy or explicitly verified mechanism. Multi-file changes need a coherent recovery set and all targets staged/verified before commit. SVN may not contain current uncommitted data; do not assume otherwise or run SVN without authorization.

## Optional audit resources

scripts/inspect_xlsx_package.py and full manifest/report examples remain for requested strict-preservation/migration work. Portable links and absence of absolute fallback metadata are different requirements. Do not clean externalLinkPath, alternateUrls, absoluteUrl or absPath during routine edits.

Report file/scope, checks, calculation/source freshness and real limitations concisely. No default validation JSON/PDF/report. Formula preservation does not imply all results or unrelated package bytes were audited.

Declared whole-scope protection, linked migration and audit evidence use [strict-audit.md](strict-audit.md); routine defaults still apply to ordinary edits.
