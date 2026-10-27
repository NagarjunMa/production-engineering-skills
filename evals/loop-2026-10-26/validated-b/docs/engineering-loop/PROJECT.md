# Inventory project context

Intent: [README](../../README.md) and the 2026-10-26 batch task. This Python
standard-library library updates caller-owned dictionaries of nonnegative integer
quantities. Valid dictionaries and integer deltas only; no I/O, persistence,
concurrency, installation or deployment requirement.

- `stock.py::adjust_stock`: canonical quantity validation, errors and single write.
- `stock.py::adjust_many`: ordered tentative updates through `adjust_stock`, then
  atomic commit on success; returns final touched values without changing input.
- `tests/test_inventory.py`: all discovered local callers, 3 single-operation and
  5 batch test methods; 27 representative input cases total.
- [Feature record](features/atomic-adjustment.md): contract A1–B4, design, current
  execution context, results and portable independent-review handoff.
- Native gate: `python3 -B -m unittest discover -s tests -v` from project root.
  Passed after implementation; current hashes/runtime: `evidence-batch.json`.
- Status: implemented and locally verified. Next step: required independent review,
  pending because further agents are prohibited. Self-review is recorded honestly.

Current source, tests, README and all existing project records were read on
2026-10-26. No manifests, lint/type/CI config, local instructions, extra production
modules or Git metadata exist. External consumers, base/branch and supported
Python range are unknown. Historical `evidence.json` and
`context-before-rename.json` reference session A and the former `inventory.py`;
they do not establish current freshness. The actual module is `stock.py`.
Verify current source and receipt rather than trusting this map alone.
