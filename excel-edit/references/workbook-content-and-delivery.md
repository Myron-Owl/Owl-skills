# Content and delivery for scoped changes

Read for operations beyond fixed value/formula/color edits.

Resolve records by authoritative paths and stable IDs; preserve machine-consumed sheet names/headers. Check uniqueness/referenced IDs only when relevant. Preserve leading-zero text, true blanks, zero, false and formula-empty results. Do not redesign calculations, add helper columns or new business assumptions during a local edit.

Prefer filling reserved data cells where appropriate. Inserting/deleting/sorting/moving data can affect formulas, names, tables, filters, validation and conditional formatting; use native Excel and check the affected dependencies. Count active records by IDs/status, not UsedRange or reserved formula rows.

Style inheritance uses a specified same-kind data row and necessary components. Preserve or deliberately set row height separately; never inherit a title's large font/height or auto-fit everything. Preserve unrelated merges; only edit the anchor of an existing merged area.

Preserve filenames/link destinations unless moving/renaming is requested. Multi-file delivery includes the intended dependency set and requested layout validation. Keep scripts/plans/previews outside formal delivery directories; same-directory transaction files are temporary and removed afterward.

Editing does not authorize SVN, downstream export or external sending. Link affected files using short clickable filenames and the actual absolute path only in each Markdown link target. Do not routinely list paths, cell addresses or changes; provide those when requested or needed to explain a conflict. Mention relevant opening/calculation/recovery limits, without a separate manifest for ordinary cell edits.
