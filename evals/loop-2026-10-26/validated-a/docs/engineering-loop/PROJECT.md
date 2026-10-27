# Inventory project context

Source of intent: [README](../../README.md). This Python standard-library library
adjusts quantities in a caller-owned dictionary. Only valid starting dictionaries
and integer deltas are in scope; there is no I/O, persistence, concurrency,
installation, or deployment requirement.

## Map and checks

- `inventory.py::adjust_stock`: the sole public operation and owner of stock rules.
- `tests/test_inventory.py::StockTests`: `unittest` contract checks and only local
  callers found by inspection/search.
- [Atomic adjustment record](features/atomic-adjustment.md): contract, current
  execution context, acceptance evidence, review handoff, and scoped lesson.
- Current status: README behavior passes local tests; required independent review
  is pending because further agents are prohibited. See the feature record and
  `evidence.json` for the exact checked source and runtime.
- Native gate, from the project root:
  `python3 -B -m unittest discover -s tests -v`.

All three original files were fully inspected on 2026-10-26. No manifests,
CI configuration, additional source, local instruction files, or `.git` directory
were present in this project. External consumers and supported Python version
range are unknown. Do not infer current evidence from this map: verify relevant
source and the feature record before subsequent work.
