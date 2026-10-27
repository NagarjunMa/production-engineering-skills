# Stock adjustments

Compact records requested for a bounded library addition. Significant risk: a
public API updates caller-owned state. No external I/O, concurrency or release.

## Contract and execution context

Session-b task, 2026-10-26: add `adjust_many(stock, adjustments)` for an ordered
list of `(sku, integer_delta)` pairs. Apply the same validation/errors as
`adjust_stock` using tentative quantities in order, allowing repeats. Intermediate
underflow is invalid even if later restored. Success updates stock and returns
final quantities for touched products only. Unknown product or underflow leaves
the entire original dictionary unchanged. Empty input returns `{}` without
mutation. Preserve `adjust_stock` and the adjustments list. README confirms valid
starting dictionaries and integer deltas; new type checking is outside scope.

Verified locations: `stock.py:adjust_stock` owns the canonical rule (preserve),
`stock.py:adjust_many` owns batch staging/commit (implemented), and
`tests/test_inventory.py` contains all local consumers: 4 existing methods and 6
new batch methods. README, PROJECT and imported lessons were read. No Git,
package, lint/type or CI configuration exists. External consumers are unknown.
The inherited map's `inventory.py` is absent; current imports verify `stock.py`.
Session-a receipts and context-before-rename are historical, not current evidence.

Design: reuse `adjust_stock` on a shallow dictionary copy; collect returned values,
then publish touched products only after all pairs succeed. One validation owner,
no new dependencies or helper layers. Copy costs O(stock size) time/memory; no
performance target justifies more staging machinery. Existing API stays intact.
Local rollback removes the addition and its tests; no deployment is involved.

## Acceptance and checks

| ID | Outcome | Test; wrong implementation rejected |
| --- | --- | --- |
| A1–A3 | Preserve single-operation success, zero, errors and unchanged state | Existing `StockTests`; compatibility regression |
| B1 | Ordered tentative quantities, repeated SKUs, touched-only finals; preserve other stock/list | `test_success_uses_tentative_quantities_and_returns_touched_products`; reading starting quantities each time or returning full stock fails |
| B2 | Zero delta/result valid; empty batch returns empty without input changes | `test_zero_adjustment_still_returns_touched_product`, `test_empty_batch_returns_empty_without_changing_inputs`; skipping zero touches fails |
| B3 | Late unknown/underflow rolls back all products; preserve list | `test_late_failure_rolls_back_every_product_and_preserves_adjustments`; incremental caller writes fail |
| B4 | Intermediate underflow fails before later restoration | `test_intermediate_underflow_is_rejected_even_if_restored_later`; netting deltas fails |
| B5 | First invalid pair determines native error type/arguments; preserve inputs | `test_first_invalid_pair_determines_error`; prechecking unknown products or sorting pairs fails |

Behavioral red/green mode. Exact native command from project root:
`python3 -B -m unittest discover -s tests -v`.
Baseline PASS: 4 methods. After adding runnable `return {}` scaffold and batch
tests, intended red: FAIL, 10 methods run, 7 assertion failures (missing errors or
wrong result); no import/setup failure. Green PASS: all 10 methods, exit 0.
In-memory compilation of both Python files PASS. SHA-256 comparison confirms the
single-adjustment function is byte-for-byte identical to the inherited source.

Implemented and locally verified. Changed `stock.py`, `tests/test_inventory.py`,
README, PROJECT, this record and LESSONS (reconciled obsolete zero advice). Added
session-b command receipt, snapshot and pending-review packet under `../evidence/`.
No files removed; historical evidence preserved. Self-review read all Python,
README and records, checked every local caller and exception path, and found no
material in-scope defect. The canonical validator is reused; the only original
stock write is after the loop. Empty updates add/change no dictionary entries.
No new shared rule or abstraction was needed. No new lesson was invented from
passing tests. Next incomplete step: the required fresh review described below.

## History and review limits

Session-a reported INV-1 (write-before-underflow validation) resolved. Current code
validates before assignment and baseline passes; original provenance is reported
history in `../evidence/commands.md`, not fresh-review evidence. Imported advice
that zero must be rejected is unsupported by README and current tests. The logging
lesson concerns a different domain; it does not establish batch atomicity.

Required fresh review remains pending because the task explicitly prohibits
delegation. Self-review cannot close this gate; reviewer rounds 0/3. Model identity
unknown. Current portable packet is `../evidence/review-packet-b.md`; final
hashes and check receipts: `../evidence/snapshot-b.json` and `commands-b.md`.
