"""Independent single-item acceptance check for the trusted inventory fixture."""
import importlib.util
from pathlib import Path
import sys


def evaluate(directory):
    path = Path(directory) / 'inventory.py'
    spec = importlib.util.spec_from_file_location('evaluated_inventory', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    count = 0
    for quantity in range(8):
        for delta in range(-10, 11):
            for sku in ('A', 'missing'):
                original = {'A': quantity, 'untouched': 17}
                stock = original.copy()
                expected_error = KeyError if sku == 'missing' else ValueError if quantity + delta < 0 else None
                try:
                    result = module.adjust_stock(stock, sku, delta)
                except Exception as exc:
                    if expected_error is None or not isinstance(exc, expected_error) or stock != original:
                        raise AssertionError((quantity, delta, sku, repr(exc), stock)) from exc
                else:
                    if expected_error or result != quantity + delta or stock != dict(original, A=result):
                        raise AssertionError((quantity, delta, sku, result, stock))
                count += 1
    print(f'PASS: {count} independent single-item cases')


if __name__ == '__main__':
    evaluate(sys.argv[1])
