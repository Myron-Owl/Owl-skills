# Fixed editor input

Both editors take one UTF-8 JSON path. Prepare plans internally; do not ask users to write them. Resolve IDs/headers before choosing cell addresses.

```json
{
  "workbook": "F:/Work/example.xlsx",
  "preconditions": [{"sheet": "Data", "range": "A2", "values": [["0012"]]}],
  "operations": [
    {"sheet": "Data", "range": "B2", "kind": "value", "before": [[10]], "values": [[12]]},
    {"sheet": "Data", "range": "B2", "kind": "font_color", "color": "#FF0000"},
    {"sheet": "Data", "range": "B2", "kind": "fill_color", "color": "#FFFF00"}
  ]
}
```

Call scripts/excel-python.cmd with -B, the absolute edit_simple.py or edit_native.py path, and the absolute plan path. Quote paths. In PowerShell put & before the quoted launcher path; in CMD omit &.

See [common operations](common-operations.md) for optional format_copies and validations. They use the same transaction; operations may be empty if one of these lists is nonempty.

## Contract

Optional native `new_sheets` is documented in [new-sheets.md](new-sheets.md). New sheets, one existing-sheet append_block and normal inputs/formulas/colors can share one transaction.

- workbook: existing absolute .xlsx/.xlsm path; simple accepts only ordinary .xlsx.
- operations: list (nonempty unless format_copies or validations is provided) of sheet/range/kind operations. Ranges are bounded uppercase A1 rectangles. Unknown fields, repeated writes to the same property/cell and more than 100,000 property writes are rejected. Values plus colors on the same cell are allowed.
- value/formula: before and values are two-dimensional matrices matching the rectangle, even for one cell. Before-values come from formula-preserving openpyxl inspection: external formulas may contain [1] link indices. Read them rather than guessing. JSON numbers, Booleans, strings and null are supported. For dates, use intended Excel serials with existing number formats. Use null for a true blank; empty text can round-trip differently and be rejected.
- formula: native only; new formulas begin with = and use Formula2 syntax. Native readback allows normal open-source/closed-source path expansion. Equivalent local worksheet quoting is also accepted token by token; literal strings, cell addresses and operators remain strict. Other unexpected normalization stops the transaction with expected/actual formulas for inspection. New spills or existing spill/legacy-array targets need a scoped operation.
- font_color/fill_color: color is #RRGGBB. Fill means solid fill. Whole-style copying and row height are available only in the explicit append_block below.
- preconditions: additional sheet/range/values matrices such as ID/header checks, without writes.
- calculation: none (default), smart, full or rebuild. Use smart for ordinary requested result updates, not rebuild just because formulas are dense.
- dependencies: existing absolute source workbook paths, upstream first. Sources are read-only and never saved. Their presence requires update_links=true. Include the relevant upstream chain, including links of declared sources.
- update_links: false by default; true requires dependencies, calculation and acceptance. Excel calculates from live cells of the already-open sources. Redundant UpdateLink calls are avoided because they fail for open sources on this machine. This is not query/data-connection refresh.
- expected_links: optional exact list of intended absolute local workbook destinations after a requested link edit. Omit to preserve existing destinations. New calculated sources must also be in dependencies.
- acceptance: sheet/range/values matrices of expected calculated values, plus optional nonnegative numeric tolerance. Required for calculation. Results are checked before saving and after sources-closed reopen. Select meaningful business results and relevant boundaries.
- timeout_seconds: default 180, range 10..3600. Bounds waiting for CalculationState after a calculation method returns. It cannot interrupt a blocking COM method; recover only this task's owned instance if Excel hangs. Never claim success for an incomplete calculation.

## Preservation and commit

Originals must be closed/writable. Conflict, unsupported target, unexpected style/formula/link change or wrong result prevents replacement. A single original-file hash detects concurrent changes without generating an inventory.

Native opens the original read-only, uses SaveCopyAs, closes original/sources, preserves the original calculation-mode metadata in the staged copy, then reopens read-only with link updating and repair disabled. openpyxl only inspects native files and never saves them. Automatic-mode files with uncalculated content edits are marked for later calculation; do not claim current cache freshness.

Formula maps compare text/attributes outside declared content writes. This is not a byte-identical package guarantee or verification of every downstream result. No automatic sorting, insertion, style copying, table expansion or validation-rule changes. For multiple fixed-edit targets, use edit_batch.py and reading-and-recovery.md; sequential recovery is not atomic commit.

## Small additions without a custom script

The native plan may include one optional `append_block` alongside ordinary operations:

```json
"append_block": {
  "sheet": "Data",
  "range": "A8:C9",
  "copy_formats_from": "A1:C2",
  "merges": ["A8:B8"],
  "row_height": 24
}
```

Only sheet/range are required. At most 2,000 cells in a workbook with at most 10,000 loaded cells; start below the last nonempty row. Existing blank styled rows may be used. This is a capability boundary, not a universal instruction about where every future model must be placed. Existing input edits elsewhere remain normal operations in the same plan. Content/formulas are written through operations with before=null for new cells; merges require writes to the anchor only. A full merged rectangle is not a content target.

copy_formats_from is a same-sheet, same-size rectangle selected for appropriate data styles. It copies formats only, never source contents or row/column dimensions. Source/destination merges, tables and conditional formatting are excluded; existing destination validation, comments and hyperlinks also need scoped handling. Formula-filled reserved rows count as occupied. Specify formulas explicitly; this does not translate/copy source formulas. Merges must be disjoint and contained in the block. row_height applies only to the block's new rows. Columns, printing and validation rules are not changed by this feature.

The executor models expected formatting in memory, applies the block and cell operations in one native Excel session, calculates once if requested, and uses its existing save/reopen checks. Old cell appearance/content and existing dimensions are compared for append edits; this extra comparison is not run for ordinary input edits. Unexpected normalization fails before replacement. Unsupported additions use scoped handling; do not try to force them through this contract.
