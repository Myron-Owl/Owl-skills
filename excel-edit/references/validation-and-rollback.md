# Validation and rollback

## Evidence layers

Validate independently:

1. **Edit evidence** — requested cells and objects changed exactly as planned.
2. **Structure evidence** — OOXML package, relationships, tables, validations, names, and merge ranges remain legal.
3. **Formula evidence** — formula text/pattern, cell kind, blank state, cached results, and errors match the contract.
4. **Native evidence** — Microsoft Excel updates permitted links, finishes calculation, saves without repair, closes, and reopens cleanly.
5. **Visual evidence** — affected user-facing sheets remain readable and correctly formatted.

One layer cannot substitute for another.

## Formula and protected-range checks

Scan at least `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, and `#N/A`. Report workbook, sheet, address, formula, cached/displayed value, and business check.

For strict protection compare each cell's:

- Formula text and formula attributes.
- Constant/formula/blank kind.
- Cached value where meaningful.
- True blank versus formula returning an empty string.
- Declared number format or style evidence.

For formula-structure protection compare formula text, native R1C1 pattern when available, formula/constant kind, formula attributes, and declared style evidence. Permit cached/displayed values to change only through the approved dependency chain; validate those values through acceptance checks rather than equality to the baseline.

For formula blocks, compare normalized R1C1 patterns when the native API can supply them. Always inspect the first, every mapping boundary, representative middle, and last row after save.

## External links

Verify:

- Formula refers to the intended real workbook and worksheet.
- External-link relationship exists and resolves to the intended file.
- Source-closed behavior is correct.
- Formula cache is fresh after native calculation.
- The complete dependency set works after relocation when required.
- Strict no-absolute-path packages contain no prohibited drive, UNC, or `file:///` targets after the final writable save.

Excel may preserve a relative primary external-link relationship and still add absolute fallback metadata during native save. For strict relative packages, inspect all of these after the last writable save:

- `xl/externalLinks/_rels/*.rels` absolute `externalLinkPath` relationships.
- `xxl21:alternateUrls` / `xxl21:absoluteUrl` nodes in `xl/externalLinks/*.xml`.
- `x15ac:absPath` metadata in `xl/workbook.xml`.

If cleanup is authorized, back up the workbook and patch only the proven absolute fallback nodes. Keep the relative primary relationship. Then reopen in Excel read-only, run acceptance checks, repeat the relocation test, audit the package again, and never save the cleaned formal workbook from Excel afterward. For package access, use a ZIP-capable API such as .NET `ZipArchive`; PowerShell `Expand-Archive` may reject an `.xlsx` extension even though the file is a ZIP package.

Make cleanup feature-detected and idempotent. Optional `externalLinks` parts or fallback nodes may already be absent; absence is not an error. The completion condition is a clean package audit with no prohibited absolute-path hits, followed by read-only reopen and relocation success.

Run the read-only package audit:

```text
python scripts/inspect_xlsx_package.py workbook.xlsx --pretty
```

If strict no-absolute-path cleanup is performed, do it after the last writable Excel save, then reopen read-only and never overwrite the formal file again.

## Visual checks

Inspect every affected sheet and each downstream presentation/result sheet. Check clipped headers and numbers, widths, row heights, formats, freezes, filters, validation prompts, conditional formatting, charts, and abnormal used ranges. Reinspect after layout repairs.

Treat image export as asynchronous. After `CopyPicture`, allow the clipboard to settle, then verify that the PNG has plausible dimensions and is not near-blank. If the workbook contains visible styled cells but the preview is blank, reactivate the sheet, copy the smallest required range, wait, and retry. A successful `Chart.Export` return value alone is not visual evidence.

If `CopyPicture` or chart export remains blank or raises `0x800A03EC`, use a read-only native fallback: set a temporary print area in memory, export the affected sheet range with `ExportAsFixedFormat` to PDF, render the PDF to an image, inspect it, close without saving, and discard the temporary files. Never save preview-only page setup changes into the formal workbook.

Also inspect business semantics that formula-error scans cannot detect: status cells unexpectedly showing failure, optional IDs changing from blank to `0`, reserved rows counted as live records, percentages or units rendered incorrectly, and valid formulas referencing a truncated range. Define valid-record counts from stable IDs and compare passed-status counts to those IDs rather than to physical row count, `UsedRange`, or the number of formula cells.

## Rollback order

On any commit, link-cleanup, reopen, or native-validation failure:

1. Stop further writes and saves.
2. Close the target workbook without saving new changes.
3. Close read-only dependencies.
4. Quit the isolated Excel instance.
5. Release automation objects.
6. Confirm target files are unlocked.
7. Restore backups to formal locations.
8. Recompute hashes and compare them with backup hashes.
9. Return `ROLLED_BACK` only after equality is proven; otherwise return the underlying failure plus incomplete-recovery details.

Never overwrite a locked file and never kill unrelated Excel processes.

## Report

Copy `assets/validation_report.example.json`. Include:

- Final state.
- Route and native Excel version.
- Exact files changed.
- Planned versus actual writes.
- Formula errors and allowed exceptions.
- Protected-range diff counts.
- Formula-structure diff counts, reported separately from permitted recalculated-value changes.
- External-link and relocation evidence.
- Backup and rollback evidence.
- Known limitations and warnings.
- Failure stage, workbook, sheet/range, operation, native error/HRESULT, and script stack when applicable.
