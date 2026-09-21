#!/usr/bin/env python3
"""Independent fixture acceptance checks; not an LLM-quality score.

Run with worker/refactor and a disposable fixture path. Any assertion fails exit 1.
This executes fixture code; use only the bundled synthetic fixtures/copies.
"""
import argparse
import importlib
import os
from pathlib import Path
import sys


def verify_worker():
    tool_type = importlib.import_module('parent').Tool
    os.environ['PEL_SYNTHETIC_CREDENTIAL'] = 'synthetic-value-only'
    for limit in (3, 10, 23):
        tool = tool_type(limit)
        for length in (limit - 1, limit, limit + 1):
            response = tool.worker('x' * length)
            assert 'PEL_SYNTHETIC_CREDENTIAL' not in response['environment_names'], response
            if length <= limit:
                assert response.get('value') == 'X' * length, (limit, length, response)
            else:
                assert 'error' in response and 'value' not in response, (limit, length, response)
    print('PASS: actual worker non-default/equality/overflow and synthetic credential cases')


def verify_refactor():
    adapters = importlib.import_module('adapters')
    plugins = importlib.import_module('plugins')
    for value, expected in [(' Test ', 'test'), ('A-B', 'a-b')]:
        assert adapters.web_tag(value) == (200, {'tag': expected})
        assert adapters.cli_tag(value) == (0, expected)
        assert plugins.run_registered(value) == expected
    assert adapters.web_tag(' ') == (422, {'error': {'message': 'empty tag'}})
    assert adapters.cli_tag(' ') == (2, 'error: empty tag')
    try:
        plugins.run_registered(' ')
    except ValueError as exc:
        assert str(exc) == 'empty tag'
    else:
        raise AssertionError('Dynamic public consumer must reject empty tag')
    print('PASS: adapter distinctions and dynamically resolved public consumer')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scenario', choices=['worker', 'refactor'])
    parser.add_argument('fixture', type=Path)
    args = parser.parse_args()
    sys.path.insert(0, str(args.fixture.resolve()))
    (verify_worker if args.scenario == 'worker' else verify_refactor)()
