# Project context

Small standard-library Python stock module. Product requirements: README.md.
Main entry point: inventory.py, adjust_stock. Tests: tests/test_inventory.py, StockTests.
No persistence, network, UI, CI, or release configuration. Feature contract and detailed code location map: [stock adjustment](features/stock-adjustment.md).

As of 2026-09-17, the documented stock adjustment behavior is implemented and verified locally: positive, negative and zero integer deltas, valid zero stock, mutation-free underflow and unknown-code errors, and selected-product-only successful mutation. The function validates a candidate quantity before assignment. Unsupported input types and concurrency remain outside scope.

Evaluation: `python3 -B -m unittest discover -s tests -v` from repository root, Python 3.11.1; four tests passed, including boundary/error subtests. The feature record retains initial baseline, observed regression failure, final source fingerprints, and acceptance mapping.

All five supplied files were inventoried and read: README.md, inventory.py, tests/test_inventory.py, this summary, and the feature record. No other source, callers, manifests, scoped instructions, or release configuration were found. No Git repository or target branch is supplied; this is a dated local snapshot, not CI or release evidence. No remaining work in the agreed scope. Reconfirm source and the feature contract on a later task.
