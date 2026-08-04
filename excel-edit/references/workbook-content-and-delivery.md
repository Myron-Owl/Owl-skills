# Workbook content and delivery conventions

Use these conventions when editing cell content, tables, validation, layout, reserved capacity, batches, or the formal delivery set.

## Understand and preserve the workbook

- Confirm the workbook's purpose, authoritative source, current and target versions, downstream consumers, and the meaning of affected sheets and fields before writing.
- Treat existing workspace changes as user-owned. Preserve unrelated values, formulas, styles, comments, validations, names, and unknown regions.
- Prefer the smallest cell, row, column, or package-node edit. Rebuild a sheet or workbook only when the user requests it, the current structure cannot support the change, or every source and regression check is known.
- Keep sheet names and machine-consumed headers stable. Use stable IDs or explicit mapping tables instead of row numbers, display labels, current sort order, or fuzzy matching.
- Keep key formula ranges bounded. Use an Excel Table, a dynamic name, or a deliberately declared capacity range when appendable lookup capacity is required.

## Preserve types and cell semantics

- Store numbers, percentages, dates, currency, Booleans, strings, and blanks as their intended types rather than display text with embedded units.
- Preserve meaningful leading-zero identifiers as text unless the workbook contract explicitly requires numeric storage. Put units in headers, dedicated fields, or notes.
- Normalize every automation payload value explicitly to string, Boolean, number, formula, or blank before crossing a library or COM boundary.
- Keep true blank, formula `""`, numeric `0`, text `"0"`, Boolean values, and lookup failure distinct. When changing blank semantics, inspect and update every downstream consumer.
- Do not let lookup failure silently become a valid zero. Handle missing keys, denominator zero, negative values, and declared bounds explicitly.
- Keep assumptions in visible parameter cells or tables instead of burying unexplained constants in long formulas. Split opaque calculations into auditable helper columns or ranges.

## Write text and formulas safely

Text beginning with `=` can be interpreted as a formula. For instructions or examples, set the cell to text explicitly or prefix the content with descriptive text that does not begin with `=`. Never place an incomplete external-reference example into a cell as formula text.

Quote sheet names containing spaces, non-ASCII characters, or formula-significant punctuation:

```excel
='Combat Parameters'!A1
```

After generated writes, verify first, last, mapping-boundary, and representative middle cells. Check both formula text/pattern and calculated or cached value according to the manifest.

## Extend workbook objects together

When adding rows or columns, update every declared dependent object together:

- formulas and named ranges;
- Excel Table boundaries;
- data-validation ranges and rules;
- conditional-format ranges and priorities;
- filters, freeze panes, number formats, and any affected charts or summaries.

Use data validation for user-entered enumerations and declared bounds. Keep core business validity in auditable formulas or external checks; conditional formatting may signal status but must not be the only implementation of business logic. Test a validation rule on one cell before applying it to a block.

## Avoid unsafe merged regions

Do not merge cells in data, calculation, filter, or export regions. Prefer a filled title band with text in its first cell. If presentation-only merges are authorized, enumerate the exact merge areas, prove that no two ranges intersect, and verify the final OOXML `mergeCells` records. Never unmerge a whole sheet merely to replace one title.

## Treat reserved capacity as inactive

- Mark reserved rows or columns explicitly as reserved, inactive, or pending.
- Do not let live-result formulas consume unconnected reserved records.
- Count live records by stable ID or explicit status, never by `UsedRange`, physical row count, or formula-filled cell count.
- Bound reserved capacity so formatting or formulas do not create an abnormally large used range.
- When activating reserved capacity, recheck formulas, tables, validation, conditional formatting, acceptance ranges, and downstream counts.

## Stage batch changes

For repeated edits, first run one to three representative cases, including a boundary case. Produce a planned before/after diff, verify the target count and payload dimensions, and list missing, duplicate, unsupported, or out-of-range objects separately before expanding to the full batch. Keep the transformation idempotent where practical; if repetition is intentionally cumulative, record the baseline and applied version.

## Preserve readable layout

- Keep titles, headers, and key results visible; freeze and filter long tables where appropriate.
- Use number formats that match the declared precision, percentage, currency, and date semantics.
- Format only used or explicitly reserved ranges. Avoid clipped text, unexplained wrapping, abnormal row heights, and giant blank used areas.
- Reinspect affected sheets and downstream presentation sheets after width, height, wrapping, freeze-pane, validation, conditional-format, or chart changes.

## Keep the formal delivery set clean

- Use stable readable filenames. Do not rename one workbook in a linked dependency set unless all authorized links and delivery instructions are updated and validated.
- Keep logs, previews, scratch data, automation scripts, backups, and recovery files outside the formal delivery directory.
- Before completion, compare the formal directory contents with the declared delivery list and deliver linked workbooks as a complete dependency set.
- Record exact files changed, reason, affected scope, validation tier, known limitations, and instructions needed to open, move, or maintain the workbook set.
