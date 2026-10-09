# Selective development checks

Use included synthetic fixtures in a task-specific temporary workspace. Optional external fixtures must be supplied explicitly; do not assume another computer's drive exists. Always test copies, leaving user workbooks and templates unchanged.

| Change | Minimum relevant check |
|---|---|
| Instructions/examples only | Read changed text/links; quick_validate only if metadata changed; no Excel |
| Quote/normalization/diagnostics | test_native_compat.py (no --fixture); add native case only if native behavior changed |
| Format copies / validations | test_native_operations.py (no Excel), then test_common_cases.py --fixtures PATH --case operations |
| Extension API | --case extension |
| Ordinary native preservation / wrap repair | --case ordinary plus test_native_compat.py negative/namespace checks |
| New worksheets | test_new_sheets.py |
| Append behavior | test_append.py |
| Reading / batch rollback | test_reading_batch.py |
| Formula links, calculation, session lifecycle, or broad transaction changes | test_editors.py --output EMPTY_ABSOLUTE_DIRECTORY --native |

Use excel-python.cmd -B and absolute script paths. Each common case opens Excel only for that case, calculates expected results and reopens through the shared executor. Do not rerun unrelated cases because a skill file changed. If several changes affect the same case, run it once after the final related change. Re-run only failed or subsequently affected checks. Retained failure copies are evidence, not a reason to rerun for more logging.

For unverified installation/consolidation integration, run test_editors.py --output ABSOLUTE_EMPTY_DIRECTORY --native once to cover ordinary edits, formulas/external links and failed acceptance preserving originals. Reuse passed evidence until changes or failures justify retesting.
