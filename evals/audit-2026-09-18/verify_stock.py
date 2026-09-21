"""Independent acceptance evaluator for the audit fixture, not part of the skill.

Usage: python3 -B evals/audit-2026-09-18/verify_stock.py /path/to/completed/fixture
Run only on the trusted isolated fixture: importing stock.py executes its code.
"""

import importlib.util
import itertools
import json
from pathlib import Path
import sys


def expected_batch(original, operations):
    """Interpret the task contract independently of the evaluated implementation."""
    quantities = dict(original)
    touched = {}
    for sku, delta in operations:
        if sku not in quantities:
            return KeyError, original, None
        candidate = quantities[sku] + delta
        if candidate < 0:
            return ValueError, original, None
        quantities[sku] = candidate
        touched[sku] = candidate
    return None, quantities, touched


def evaluate(directory):
    module_path = Path(directory).resolve() / "stock.py"
    spec = importlib.util.spec_from_file_location("audited_stock", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    operations = [(sku, delta) for sku in ("A", "B", "missing") for delta in (-2, 0, 2)]
    count = 0
    for qa, qb in itertools.product(range(3), repeat=2):
        for length in range(4):
            for sequence in itertools.product(operations, repeat=length):
                original = {"A": qa, "B": qb, "untouched": 7}
                stock = original.copy()
                changes = list(sequence)
                error, expected_stock, expected_result = expected_batch(original, sequence)
                try:
                    result = module.adjust_many(stock, changes)
                except Exception as exc:
                    if error is None or not isinstance(exc, error):
                        raise AssertionError((original, sequence, "unexpected error", repr(exc))) from exc
                else:
                    assert error is None, (original, sequence, "required error absent")
                    assert result == expected_result, (original, sequence, result, expected_result)
                assert stock == expected_stock, (original, sequence, stock, expected_stock)
                assert changes == list(sequence), "adjustments input was mutated"
                count += 1

    # Protect the existing single-item contract as well as the new feature.
    single_count = 0
    for quantity in range(3):
        for sku in ("A", "missing"):
            for delta in range(-3, 4):
                original = {"A": quantity, "untouched": 7}
                stock = original.copy()
                error, expected_stock, _ = expected_batch(original, [(sku, delta)])
                try:
                    result = module.adjust_stock(stock, sku, delta)
                except Exception as exc:
                    assert error is not None and isinstance(exc, error), repr(exc)
                else:
                    assert error is None and result == quantity + delta
                assert stock == expected_stock
                single_count += 1
    return {"status": "passed", "batch_cases": count, "single_item_cases": single_count}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: verify_stock.py FIXTURE_DIRECTORY")
    print(json.dumps(evaluate(sys.argv[1]), sort_keys=True))
