# Inventory project context

Python standard-library inventory library for callers adjusting a dictionary of
nonnegative integer quantities. [README](../../README.md) is the product contract;
integer deltas and valid dictionaries only. No UI, persistence, external services,
concurrency, installation, or deployment. Runtime observed: Python 3.11.1.

The entire initial project was inspected: `inventory.py` owns `adjust_stock` and
the state transition; `tests/test_inventory.py` is its only local caller and uses
`unittest`; `README.md` defines behavior and the native command. No package, CI,
or Git metadata was present. External callers are unknown.

Run from the project root: `python3 -B -m unittest discover -s tests -v`.
See [stock adjustments](features/stock-adjustments.md) for current contract,
locations, checks, review status, and next step. No other work is authorized.

Freshness: inspected the raw workspace on 2026-10-26; no Git revision is available.
Final source hashes and command receipts are in `evidence/`.
