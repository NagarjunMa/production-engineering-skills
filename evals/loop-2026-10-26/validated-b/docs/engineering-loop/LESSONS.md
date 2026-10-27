# Scoped project lessons

## Stock state checks

Historical INV-1 wrote a negative candidate before rejecting it. The current
single-operation regression compares the entire dictionary before/after failure.
For the batch operation, failures after earlier successful tentative updates must
also compare the entire original dictionary. Current regressions cover unknown
products, later underflow and repeated-SKU intermediate underflow. Scope: this
caller-owned integer dictionary API; this establishes no database/concurrency rule.

## Stale context correction

The imported map referenced `inventory.py`; current inventory and imports establish
`stock.py`. Revalidate source locations and receipts after a rename. The old
receipt remains historical; the current receipt is `evidence-batch.json`.

## Imported hypotheses and unrelated notes

The old claim that zero stock should be rejected has unknown provenance and is
unsupported here: README explicitly allows zero, and single/batch tests cover it.
For an append-only audit-log writer, flushing may be required by that writer's
durability contract. It creates no logging or stock-mutation requirement here.
