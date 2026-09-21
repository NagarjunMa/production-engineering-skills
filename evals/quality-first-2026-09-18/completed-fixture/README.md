# Parcel quotes

A small Python library with web and CLI entry points. No persistence or network.
`parcel.policy.fee_cents` owns the shipping fee rule: nonnegative integer subtotals only (booleans invalid); delivery is 499 cents below 5000 cents and free from 5000.
Web quote success: {"status": 200, "fee_cents": fee}; invalid input: {"status": 400, "error": "invalid subtotal"}.
CLI success: "Shipping: <fee> cents"; invalid input: "Error: invalid subtotal". Those distinct error/output contracts are intentional.

Requested new behavior: web_quotes(subtotals) returns web-quote responses in input order, validating each independently; one invalid subtotal must not prevent later quotes. Empty input returns an empty list. Inputs are not mutated. Preserve existing entry points and fee policy.

Checks: python3 -B -m unittest discover -s tests -v
