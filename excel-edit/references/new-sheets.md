# New worksheets in the native editor

Declared new row heights are also checked through Excel after reopening: a native height of 26 can be stored as 26.1 in OOXML. The executor reapplies declared new heights after writing text; it does not auto-fit old rows.

Widths use native Excel `ColumnWidth` units and are verified natively after reopening. Do not substitute openpyxl's stored `width`: it includes padding and may differ (for example 18 versus 18.625). Existing-sheet dimensions retain their normal preservation checks.

Use the normal edit_native.py plan and launcher. Add optional `new_sheets`:

```json
"new_sheets": [{
  "name": "Phase2",
  "range": "B2:H30",
  "formats": [{"source_sheet": "Phase1", "source_range": "B7:D8", "range": "B7:D8"}],
  "merges": ["B2:H2"],
  "row_height": 24,
  "column_widths": {"B": 24, "C": 16, "D": 20}
}]
```

Only name/range are required. Up to five new, case-insensitively unique sheet names, each region at most 5,000 cells; existing workbook at most 20,000 loaded cells. Sheets are added after existing sheets. Write values/formulas through normal operations, with before=null for new cells and normal calculation/acceptance fields.

Format sources are same-size rectangles in pre-existing sheets, without tables or conditional formatting. A source may contain complete merged titles if each corresponding destination merge is explicitly declared; partial merged sources are rejected. Only formats are copied, never contents or formulas. Explicit merges must be disjoint and inside the new region; write only anchors. Colors use normal operations. Dimensions affect new sheets only; use Excel-representable row heights and native ColumnWidth values.

One existing-sheet append_block may accompany this to append usage notes in the same transaction. Its existing restrictions apply. No automatic printing changes, PDF export, pagination, images, validation-rule creation or formula translation. Those need actual requirements and scoped handling.

The existing transaction creates sheets, applies formats and edits in one native session, calculates as needed, saves/reopens and checks. It compares old cells, styles, dimensions and merges, accounting for declared edits and the append block. Only the proven loss of wrapping on unchanged merged anchors is restored in the staged package before native reopen. Other unexpected normalization prevents replacement. Old page settings and data validation metadata are checked before replacement. This is not byte-for-byte package preservation.

Use the documented contract instead of reading implementation source for each task. Run scripts/test_new_sheets.py only during development after related changes.
