# Inventory project context

Python standard-library inventory library for callers adjusting a dictionary of
nonnegative integer quantities. [README](../../README.md) is the product contract;
integer deltas and valid dictionaries only. No UI, persistence, external services,
concurrency, installation, or deployment. Runtime observed: Python 3.11.1.

The current source and local callers were inspected: `stock.py` owns `adjust_stock`
and the atomic `adjust_many`; `tests/test_inventory.py` is the only local caller and uses
`unittest`; `README.md` defines behavior and the native command. No package, CI,
or Git metadata was present. External callers are unknown.

Run from the project root: `python3 -B -m unittest discover -s tests -v`.
See [stock adjustments](features/stock-adjustments.md) for current contract,
locations, checks, review status, and next step. No other work is authorized.

Freshness: revalidated in session-b on 2026-10-26; no Git revision exists. The
inherited map referenced absent `inventory.py`; current imports verify `stock.py`.
Session-a receipts and pre-rename context are historical. Current evidence is
in `evidence/commands-b.md` and `evidence/snapshot-b.json`.
