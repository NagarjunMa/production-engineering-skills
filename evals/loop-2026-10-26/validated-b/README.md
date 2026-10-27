# Inventory library

This is a standard-library Python library. `stock.adjust_stock(stock, sku, delta)`
updates a caller-owned dictionary of nonnegative integer quantities. Existing
products accept positive, zero, and negative integer adjustments; zero resulting
stock is valid. Return and store the resulting quantity. An unknown product raises
`KeyError`; a negative result raises `ValueError`. Every rejected operation must
leave the entire dictionary unchanged. Preserve other products.

Only integer deltas and valid starting dictionaries are in scope. No UI, database,
network, concurrency, installation, or deployment is required. Native check:
`python3 -B -m unittest discover -s tests -v` from this directory.

`stock.adjust_many(stock, adjustments)` applies an ordered list of `(sku, delta)`
pairs using the same rules on tentative quantities. Repeated products are
sequential: every intermediate quantity must be nonnegative. If any adjustment
fails, the entire original dictionary stays unchanged. Success updates the
original dictionary and returns a new dictionary containing only final quantities
for touched products, including zero-delta products. Empty input returns `{}`.
The adjustment list is never modified.
