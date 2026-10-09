# Engine selection

| Situation | Route | Routine verification |
|---|---|---|
| Ordinary formula-free .xlsx, fixed values/static colors | scripts/edit_simple.py | Before-values, saved local values/types/styles/dimensions |
| Formulas or workbook external links, including color-only edits | scripts/edit_native.py | Local checks, unchanged formulas/link targets and native reopen; calculation only if needed |
| VBA workbook, preserve without executing VBA | Native | Macros disabled; fixed editor rejects signed/ActiveX/XLM cases |
| Read-only question | Read-only inspection | No editor or saving |
| Insertion/move/sort, table/rule/name changes, spill/array targets | Scoped native extension | Affected objects/references, boundaries and expected results |
| Connections/model, ActiveX, signatures, encryption, strict relocation | Scoped native workflow | Only applicable feature/refresh/migration checks |

Simple mode scans feature markers once and rejects formulas, external links and unsupported features before writing. Unsupported-library warnings are errors. Ordinary styles, merges, data validation and conditional formatting elsewhere do not imply a full audit.

Native fixed editing accepts .xlsx/.xlsm and ordinary fixed formula/value/color changes. It preserves existing dynamic arrays but rejects changes to spill or legacy-array targets. It does not manage connections, models, ActiveX, XLM, signatures or encrypted files.

An executor rejection calls for inspecting and scoping the operation, not blindly enabling every legacy audit. Engine selection is automatic within authorization; do not request an advanced-route confirmation just because formulas/links exist. Use [edit-plan.md](edit-plan.md) for executor input.

Engine and verification scope are independent. Whole-scope protection, linked migration or audit evidence selects [strict-audit.md](strict-audit.md). If native is unavailable, continue only safe read-only preparation and report the missing capability; do not write through weaker tools.
