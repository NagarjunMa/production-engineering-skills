# Project context

Small standard-library Python stock module. Existing requirements: README.md;
current batch feature requested in the isolated task on 2026-09-18.
Main entry point: `stock.py:adjust_stock`; `adjust_many` in the same module stages sequential batch adjustments and
commits touched quantities only after all pairs validate. Tests: `tests/test_inventory.py:StockTests` and BatchStockTests.
Feature contract and detailed evidence: [stock adjustment](features/stock-adjustment.md).

Freshness: source, tests, README, and prior records read completely 2026-09-18.
The earlier record's inventory.py path is stale; current tests import stock.py.
The earlier validate-before-write lesson remains applicable and was verified
against adjust_stock. No other callers, dependencies, CI, or release targets found.
Installed skill packages were inventoried; only the explicitly invoked .agents
skill and applicable references were read. No host auto-discovery is claimed.

Baseline: `python3 -B -m unittest discover -s tests -v` passed 4 tests on Python
3.11.1. Final batch and compatibility suite passed all 11 tests on 2026-09-18;
ordered repeated products, zero/empty cases, and complete state preservation on
underflow or unknown codes are covered. No remaining in-scope work. All supplied files are untracked
in this fixture's Git worktree; no integration branch or release is requested.
Unsupported types and concurrency remain outside scope.
