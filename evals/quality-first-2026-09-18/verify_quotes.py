"""Independent contract checks for trusted disposable parcel fixtures.

Usage: python3 -B verify_quotes.py FIXTURE_DIRECTORY
Do not use -O: assertions implement the checks. Importing a fixture executes it.
"""

import importlib
import itertools
import json
from pathlib import Path
import sys


def expected(subtotal):
    if type(subtotal) is not int or subtotal < 0:
        return {"status": 400, "error": "invalid subtotal"}
    return {"status": 200, "fee_cents": 0 if subtotal >= 5000 else 499}


def evaluate(directory):
    sys.path.insert(0, str(Path(directory).resolve()))
    web = importlib.import_module("parcel.web")
    cli = importlib.import_module("parcel.cli")
    values = [-1, 0, 1, 4999, 5000, 5001, True, None, "100", 1.5]
    batches = 0
    for length in range(4):
        for sequence in itertools.product(values, repeat=length):
            inputs = list(sequence)
            result = web.web_quotes(inputs)
            assert result == [expected(value) for value in sequence], (sequence, result)
            assert inputs == list(sequence), "Input was mutated"
            batches += 1
    for value in values:
        want = expected(value)
        assert web.web_quote(value) == want
        message = (
            f"Shipping: {want['fee_cents']} cents"
            if want["status"] == 200
            else "Error: invalid subtotal"
        )
        assert cli.cli_quote(value) == message
    return {"status": "passed", "batch_cases": batches, "existing_entrypoint_cases": len(values) * 2}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: verify_quotes.py FIXTURE_DIRECTORY")
    print(json.dumps(evaluate(sys.argv[1]), sort_keys=True))
