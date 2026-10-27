#!/usr/bin/env python3
"""Check current skill/artifact fingerprints and recorded forward-test outcomes, not their truth."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/production-engineering-loop'
REQUIRED = {'implementation', 'continuation', 'review-only'}


def hashes(directory):
    return {path.relative_to(directory).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(directory.rglob('*')) if path.is_file()
            and '__pycache__' not in path.parts and path.suffix != '.pyc'}


def validate(root, skill, evidence):
    root = root.resolve()
    errors = []
    if not isinstance(evidence, dict) or type(evidence.get('schema_version')) is not int or evidence['schema_version'] != 1:
        return ['Unsupported behavioral evidence schema']
    if evidence.get('skill_sha256') != hashes(skill):
        errors.append('Skill changed or evidence is incomplete: run fresh behavioral evaluations')
    runs = evidence.get('runs')
    if not isinstance(runs, list) or not all(isinstance(run, dict) for run in runs):
        return errors + ['Runs must be a list of objects']
    ids = [run.get('id') for run in runs]
    if any(not isinstance(name, str) for name in ids) or set(ids) != REQUIRED or len(ids) != len(REQUIRED):
        errors.append('Record exactly implementation, continuation, and review-only scenarios')
    for run in runs:
        name = str(run.get('id'))
        if run.get('result') != 'passed' or run.get('fresh_context') is not True:
            errors.append(name + ': scenario has not passed in a fresh context')
        for field in ('host', 'task', 'observations'):
            if not isinstance(run.get(field), str) or not run[field].strip():
                errors.append(name + ': missing ' + field)
        artifacts = run.get('artifacts')
        if not isinstance(artifacts, dict) or not artifacts:
            errors.append(name + ': retain inspected artifacts')
        else:
            for relative, expected in artifacts.items():
                if not isinstance(relative, str):
                    errors.append(name + ': invalid artifact path')
                    continue
                path = PurePosixPath(relative)
                target = root / relative
                if path.is_absolute() or '..' in path.parts or '\\' in relative or not target.resolve().is_relative_to(root):
                    errors.append(name + ': artifact escapes repository')
                elif not target.is_file() or target.is_symlink():
                    errors.append(name + ': missing/unsupported artifact ' + relative)
                elif hashlib.sha256(target.read_bytes()).hexdigest() != expected:
                    errors.append(name + ': artifact changed: ' + relative)
        checks = run.get('checks')
        if not isinstance(checks, list) or not checks:
            errors.append(name + ': no verification recorded')
        else:
            for check in checks:
                if (not isinstance(check, dict) or not isinstance(check.get('command'), str)
                        or not check['command'].strip() or check.get('result') != 'passed'
                        or type(check.get('exit_code')) is not int or check['exit_code'] != 0):
                    errors.append(name + ': verification is missing or has not passed')
    if (not isinstance(evidence.get('limitations'), list) or not evidence['limitations']
            or any(not isinstance(item, str) or not item.strip() for item in evidence['limitations'])):
        errors.append('Record limitations; this is not a quality guarantee')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, default=ROOT / 'evals/loop-2026-10-26/results.json')
    args = parser.parse_args()
    try:
        errors = validate(ROOT, SKILL, json.loads(args.evidence.read_text(encoding='utf-8')))
        if errors:
            print('\n'.join(errors), file=sys.stderr)
            return 1
        print('PASS: current skill and retained forward-test records match; execution claims still require evidence review')
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
