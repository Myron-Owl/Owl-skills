# PowerShell, COM, and generated-formula pitfalls

Use this reference for native Excel automation from Windows PowerShell, especially when formulas or links are generated dynamically.

## Encoding and execution

- Treat Windows PowerShell 5, UTF-8 without BOM, and non-ASCII sheet names as an unsafe combination.
- Parse scripts before Excel starts. Load explicitly with `Get-Content -Raw -Encoding UTF8` and `ScriptBlock.Create` when BOM handling is uncertain.
- Ensure parser failures terminate the check; a later success message must not hide a non-terminating error.
- A successful parse is not an execution proof. Also lint command/argument adhesion such as `return$s`, `throw"message"`, `Rel$r`, a quoted range immediately followed by `$rows`, or adjacent quoted sheet-name arguments. Exercise failure and rollback branches without Excel so diagnostic code is not first executed during a real failure.
- Give the outer command enough time for Excel calculation, close, reopen, and relocation checks. If a timeout interrupts execution, inspect hashes, backups, locks, reports, and only the process created by the transaction before retrying.

## Offline payload gate

Before creating an Excel COM object:

1. Build dynamic headers and representative first, middle, last, and boundary rows in memory.
2. Assert every row has the expected column count.
3. Convert every block to the same two-dimensional matrix type used at the COM boundary and assert it matches the target A1 range.
4. Test single-row and multi-row paths independently.
5. Serialize the success report and intentionally execute the failure/rollback report path.

Do not rely on compact expressions such as `$headers += @($key+'Min',$key+'Max')` without a count assertion. PowerShell expression binding can produce a different element count than intended. Prefer explicit per-element appends in fragile builders.

When invoking the bundled preflight script, pass the automation script itself with `-ScriptPath` as well as the manifest and payload. A payload-only run can validate data while leaving the actual automation script unparsed. When executing a loaded script block, forward every mandatory parameter explicitly; successful `ScriptBlock.Create` only proves parsing, not parameter binding.

## Formula generation

PowerShell can reinterpret an Excel range while interpolating variables:

```powershell
# Unsafe: may become COUNT(D5)
"=COUNT(D$r:S$r)"

# Safe
"=COUNT(D${r}:S${r})"
```

Require three checks:

1. Assert the generated string contains the intended token such as `D5:S5`.
2. Read the formula back from Excel after writing.
3. Validate the business predicate, not only the absence of `#REF!` or other formula errors.

Use explicit blank preservation for optional fields:

```excel
=IF(Source!A1="","",Source!A1)
```

A bare `=Source!A1` can convert a truly blank source into numeric `0`. Keep true blank, formula `""`, numeric zero, and lookup failure distinct in both formulas and regression evidence.

Analyze the formula domain before writing. Test denominator zero, `-100%` multipliers, negative values, missing lookup keys, empty inputs, and both sides of each threshold. Declare where rounding occurs; avoid intermediate rounding unless required, because repeated rounding across formula layers can prevent exact source reproduction without producing an Excel error.

Treat lookup capacity as an interface contract. For registries expected to grow, prefer structured table columns or dynamic names; use whole-column lookup references when cross-workbook portability and append-only growth matter more than the modest calculation cost. Do not encode the current last data row in every consumer. Keep lookup capacity separate from live-record validation: whole-column lookup does not authorize whole-column counts, formula fills, or acceptance ranges.

When importing numeric text, distinguish a range separator from a negative sign. Include parser fixtures for positive ranges (`60-65`), negative values (`-5`), negative ranges, decimals, and blanks before converting source data into a workbook payload.

## COM operation boundaries

- Open workbooks before setting `Application.Calculation`.
- Unmerge only known title or merge areas; avoid whole-sheet `Cells.UnMerge()` and broad `UsedRange.UnMerge()` calls.
- Test `Validation.Add` on one cell. Supply both bounds for `between`, use a single-bound operator for `>=` or `<=`, and prefer formula-based business validation when input validation is optional.
- Write rectangular matrices and verify dimensions before assignment.
- Resolve a sheet by exact identity without treating every COM exception as “sheet missing.” A broad lookup `catch` can hide a real COM failure and then create a duplicate-name sheet. Enumerate existing sheet names or distinguish the missing-item condition explicitly.
- Suppress non-diagnostic method results with `[void]`.

## Status and reserved rows

Formula-filled reserved rows are not live records. Prefer:

```excel
=COUNTIF(StatusRange,"通过")=COUNTA(IdRange)
```

Do not derive valid-record counts from `UsedRange`, physical row count, or formula-cell count. Visually inspect status and configuration sheets because legal formulas can still produce semantically wrong states.

Design validation formulas around field semantics, not a convenient expected constant. Separate these questions:

- Is a required result present and numeric?
- Is it inside the legal range?
- Did it inherit a default or use a valid explicit override?
- Is the stored representation Boolean, numeric `1/0`, text, or a formula result?

Do not use `COUNTIF(range,TRUE)` until the actual cell kind and cached representation have been inspected. Formula chains, COM, and OOXML may expose a logical-looking result as numeric `1/0`; validate the declared storage contract or use explicit per-row predicates.

## Strict relative links

After the final writable native save, scan for:

- drive-letter, UNC, and `file:///` targets;
- absolute external-link fallback relationships;
- `xxl21:alternateUrls`;
- workbook `x15ac:absPath` metadata.

When strict cleanup is required, inspect before patching. Treat an absent optional external-link part as “nothing to clean,” not as failure. Patch only verified fallback nodes, preserve the relative primary link, then require a zero-hit absolute-path audit, read-only native reopen, and relocation test. Cleanup must be idempotent and must not save from Excel afterward.

## Diagnostic contract

Maintain a stage variable throughout the transaction. On the first failure, report the stage, workbook, sheet/range, attempted operation, error/HRESULT, formula or displayed value where relevant, and script stack. Roll back only after closing and releasing the isolated Excel objects, then verify the restored hash.

Keep the report schema stable: use an empty array rather than `null` for zero formula errors, set the stage before every phase including final verification, and suppress helper return values. When many cells share one root-cause formula pattern, keep the full machine-readable list but summarize diagnostics by sheet and normalized formula pattern.
