#!/usr/bin/env python3
"""Replay trusted fixtures, including negative controls. This does not run an AI model."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/production-engineering-loop'

# Each case names a real evaluator and a trusted fixture; no commands come from memory.
CASES = (
    ('stock-skill', 'evals/audit-2026-09-18/verify_stock.py',
     'evals/audit-2026-09-18/completed-fixtures/with-skill', [], 0, '"status": "passed"'),
    ('stock-baseline', 'evals/audit-2026-09-18/verify_stock.py',
     'evals/audit-2026-09-18/completed-fixtures/baseline', [], 0, '"status": "passed"'),
    ('quotes', 'evals/quality-first-2026-09-18/verify_quotes.py',
     'evals/quality-first-2026-09-18/completed-fixture', [], 0, '"status": "passed"'),
    ('worker-skill', 'evals/review-loop-2026-09-20/verify_outcomes.py',
     'evals/review-loop-2026-09-20/candidate', ['worker'], 0, 'PASS:'),
    ('worker-baseline', 'evals/review-loop-2026-09-20/verify_outcomes.py',
     'evals/review-loop-2026-09-20/baseline/worker-fixture', ['worker'], 0, 'PASS:'),
    ('refactor-skill', 'evals/review-loop-2026-09-20/verify_outcomes.py',
     'evals/review-loop-2026-09-20/candidate-refactor', ['refactor'], 0, 'PASS:'),
    ('refactor-baseline', 'evals/review-loop-2026-09-20/verify_outcomes.py',
     'evals/review-loop-2026-09-20/baseline/refactor-fixture', ['refactor'], 0, 'PASS:'),
    ('broken-worker-control', 'evals/review-loop-2026-09-20/verify_outcomes.py',
     'evals/review-loop-2026-09-20/baseline/raw-worker-start', ['worker'], 1, 'AssertionError: (3, 4,'),
    ('current-learning-single', 'evals/loop-2026-10-26/verify_single.py',
     'evals/loop-2026-10-26/validated-a', [], 0, 'PASS: 336 independent single-item cases'),
    ('current-learning-batch', 'evals/audit-2026-09-18/verify_stock.py',
     'evals/loop-2026-10-26/validated-b', [], 0, '"status": "passed"'),
    ('current-learning-broken-control', 'evals/loop-2026-10-26/verify_single.py',
     'evals/loop-2026-10-26/starting', [], 1, 'AssertionError: (0, -10,'),
)


def fingerprints():
    paths = set(SKILL.rglob('*')) | {Path(__file__).resolve()}
    for _, evaluator, fixture, *_ in CASES:
        paths.add(ROOT / evaluator)
        paths.update((ROOT / fixture).rglob('*'))
    return {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(paths) if path.is_file()
            and '__pycache__' not in path.parts and path.suffix != '.pyc'}


def run_case(name, command, cwd, expected, marker):
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=60)
        passed = result.returncode == expected and marker in result.stdout + result.stderr
        return {'id': name, 'result': 'passed' if passed else 'failed',
                'expected_exit': expected, 'actual_exit': result.returncode,
                'stdout': result.stdout, 'stderr': result.stderr}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {'id': name, 'result': 'blocked', 'reason': type(exc).__name__}


def evaluate():
    before = fingerprints()
    checks = []
    with tempfile.TemporaryDirectory(prefix='pel-replay-') as temporary:
        scratch = Path(temporary)
        for name, evaluator, fixture, arguments, expected, marker in CASES:
            copied = scratch / name
            shutil.copytree(ROOT / fixture, copied, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            command = [sys.executable, '-B', str(ROOT / evaluator), *arguments, str(copied)]
            check = run_case(name, command, copied, expected, marker)
            check['command'] = ['python', '-B', evaluator, *arguments, '<fixture>']
            checks.append(check)
        for evaluator in sorted({case[1] for case in CASES if 'verify_single.py' not in case[1]}):
            check = run_case('optimization-control:' + evaluator,
                             [sys.executable, '-B', '-O', str(ROOT / evaluator)],
                             scratch, 1, 'optimization disables acceptance checks')
            check['command'] = ['python', '-B', '-O', evaluator]
            checks.append(check)
        # Tracebacks retain useful evidence but never the caller's local root.
        for check in checks:
            for stream in ('stdout', 'stderr'):
                check[stream] = check.get(stream, '').replace(str(ROOT), '<repository>').replace(str(scratch), '<scratch>')
    unchanged = before == fingerprints()
    return {'schema_version': 1, 'kind': 'fixture-replay', 'python': platform.python_version(),
            'executed_at': datetime.now(timezone.utc).isoformat(),
            'input_sha256': before, 'source_unchanged': unchanged,
            'result': 'passed' if unchanged and all(c['result'] == 'passed' for c in checks) else 'failed',
            'checks': checks,
            'limitations': ['Replays retained outputs, not fresh agent behavior or a quality-improvement benchmark.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='New report file outside the repository; otherwise print JSON')
    args = parser.parse_args()
    try:
        if args.output and args.output.resolve().is_relative_to(ROOT):
            raise ValueError('Keep replay receipts outside source')
        if args.output and args.output.exists():
            raise ValueError('Refusing to overwrite an existing receipt')
        report = evaluate()
        rendered = json.dumps(report, indent=2, ensure_ascii=True) + '\n'
        if args.output:
            with args.output.open('x', encoding='utf-8') as destination:
                destination.write(rendered)
            print(report['result'].upper() + ': ' + str(len(report['checks'])) + ' fixture/control checks; receipt written')
        else:
            print(rendered, end='')
        return 0 if report['result'] == 'passed' else 1
    except (OSError, ValueError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
