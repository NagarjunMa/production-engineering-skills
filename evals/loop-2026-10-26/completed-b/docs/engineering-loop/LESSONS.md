# Imported project notes

## Superseded historical claim

An old note says stock quantities equal to zero should be rejected. Its source and
applicability were unknown. Status: superseded for this library on 2026-10-26.
README explicitly permits zero; `StockTests.test_successful_adjustments` and
`BatchStockTests.test_zero_adjustment_still_returns_touched_product` pass with
zero quantities. Do not apply the old claim to these stock APIs.

## Separate logging lesson

For an append-only audit-log writer, flush each completed record when the durability
contract requires it. Applies only to a log writer. It establishes no stock-mutation
or batch-atomicity rule. No logging feature is requested here.
