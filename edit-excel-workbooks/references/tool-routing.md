# Tool routing

## Decision table

| Condition | Required route | Permitted supporting tools |
|---|---|---|
| Existing workbook with cross-workbook formulas | Native Microsoft Excel session | Read-only OOXML inspection, diff scripts |
| `.xlsm`, VBA, Power Query, Power Pivot, data model, external data connection | Native Microsoft Excel session | Read-only inventory tools |
| Must preserve link relationships or cached values | Native Microsoft Excel session | Package audit before and after |
| Dense modern formulas, dynamic arrays, shared formulas | Prefer native Microsoft Excel; native validation mandatory | Structure-only formula inspection |
| Small text/style edit in a complex linked workbook | Native Excel or audited surgical OOXML patch | Never full third-party import/export without proof |
| New simple workbook without links, macros, model, or native parity requirement | Standalone authoring is allowed | Native final calculation when formulas matter |
| Read-only question or audit | Read-only inspection | Do not save or export unless requested |
| Exact OOXML node change with known package part | Surgical package patch after backup | Native read-only reopen and package diff |

## Native surfaces

Prefer, in order of fit:

1. A verified live Microsoft Excel session with workbook-aware read/write commands.
2. An isolated local Microsoft Excel automation instance controlled through COM or a trusted wrapper.
3. Manual Excel execution using a generated dry-run plan when automation is unavailable.

Do not claim that a file library, renderer, LibreOffice, or stale formula cache is Microsoft Excel truth.

## Downgrade rule

If the required native surface is unavailable:

1. Continue only with safe read-only inventory and dry-run planning.
2. Do not modify the formal workbook through a weaker route.
3. State the missing capability.
4. Mark any completed audit `PASS_STRUCTURE_ONLY`, never `PASS_NATIVE`.

## Tool behavior to avoid

- Re-serializing a complex existing workbook merely to alter a few cells.
- Using a library that reads formula strings but cannot calculate them as final truth.
- Saving after a strict absolute-path cleanup that Excel may undo.
- Opening an untrusted macro workbook programmatically before setting macro security.
- Editing through screen clicks when workbook-aware APIs are available.

