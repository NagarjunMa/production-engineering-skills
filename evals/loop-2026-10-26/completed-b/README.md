# Inventory library

This is a standard-library Python library. `stock.adjust_stock(stock, sku, delta)`
updates a caller-owned dictionary of nonnegative integer quantities. Existing
products accept positive, zero, and negative integer adjustments; zero resulting
stock is valid. Return and store the resulting quantity. An unknown product raises
`KeyError`; a negative result raises `ValueError`. Every rejected operation must
leave the entire dictionary unchanged. Preserve other products.

`stock.adjust_many(stock, adjustments)` accepts an ordered list of `(sku, delta)`
pairs. It applies the same rules to tentative quantities, allowing repeated SKUs.
Every intermediate quantity must be nonnegative. On success, update stock and
return final quantities for touched products only. Unknown products or underflow
leave the entire stock dictionary unchanged. An empty list returns `{}` without
changing stock. The adjustments list is preserved on success and failure.

Only integer deltas and valid starting dictionaries are in scope. No UI, database,
network, concurrency, installation, or deployment is required. Native check:
`python3 -B -m unittest discover -s tests -v` from this directory.
