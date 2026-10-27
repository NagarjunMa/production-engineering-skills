#!/usr/bin/env python3
"""Fingerprint reviewed project memory and selected sources; never edit or execute them.

Python 3.10+, standard library, no Git required. Capture prints a JSON receipt.
Exit 0: current; 1: changed/missing evidence; 2: invalid input or capture failure.
"""
import argparse
import json
from pathlib import Path
import sys

# Read-only invocation must not create a cache in the installed skill directory.
sys.dont_write_bytecode = True
from review_evidence import digest, fingerprint, relative_path


def collect(root, paths):
    paths = {relative_path(path) for path in paths}
    return {path: fingerprint(root, path) for path in sorted(paths)}


def capture(root, record, sources):
    record = relative_path(record)
    paths = [record, *sources]
    files = collect(root, paths)
    if any(value['kind'] != 'file' for value in files.values()):
        raise ValueError('Memory and selected evidence must be existing regular files, not symlinks')
    if len(files) < 2:
        raise ValueError('Select at least one evidence file different from the memory record')
    if collect(root, paths) != files:
        raise ValueError('Files changed during capture; pause writers and retry')
    body = {'schema_version': 1, 'record': record, 'files': files}
    return dict(body, snapshot_id=digest(body))


def load_receipt(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        raise ValueError('Unsupported memory receipt schema')
    record = relative_path(data['record'])
    files = data['files']
    if not isinstance(files, dict) or len(files) < 2 or record not in files:
        raise ValueError('Receipt must include the memory record and selected evidence')
    for name, value in files.items():
        if relative_path(name) != name or not isinstance(value, dict) or value.get('kind') != 'file':
            raise ValueError('Invalid receipt file entry')
        sha = value.get('sha256')
        if not isinstance(sha, str) or len(sha) != 64 or any(c not in '0123456789abcdef' for c in sha):
            raise ValueError('Invalid file fingerprint')
        if type(value.get('executable')) is not bool:
            raise ValueError('Invalid executable flag')
    if data.get('snapshot_id') != digest({k: v for k, v in data.items() if k != 'snapshot_id'}):
        raise ValueError('Memory receipt integrity mismatch')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='action', required=True)
    capture_parser = commands.add_parser('capture', help='Print a receipt after reviewing the record and its sources')
    capture_parser.add_argument('--record', required=True, help='Repository-relative memory document')
    capture_parser.add_argument('--source', action='append', required=True, help='Selected repository-relative evidence file; repeat as needed')
    check_parser = commands.add_parser('check', help='Report changed evidence without refreshing the receipt')
    check_parser.add_argument('--receipt', type=Path, required=True)
    for command in (capture_parser, check_parser):
        command.add_argument('--repo', type=Path, required=True)
    args = parser.parse_args()
    try:
        root = args.repo.resolve(strict=True)
        if not root.is_dir():
            raise ValueError('--repo must be a project directory')
        if args.action == 'capture':
            print(json.dumps(capture(root, args.record, args.source), indent=2, ensure_ascii=True))
            return 0
        receipt = load_receipt(args.receipt)
        if args.receipt.resolve() in {root / path for path in receipt['files']}:
            raise ValueError('Receipt must be separate from its memory and source files')
        current = collect(root, receipt['files'])
        if collect(root, receipt['files']) != current:
            raise ValueError('Files changed during check; pause writers and retry')
        changed = [path for path in current if current[path] != receipt['files'][path]]
        if changed:
            print('STALE: revalidate memory before refreshing its receipt. Changed paths: '
                  + json.dumps(changed), file=sys.stderr)
            return 1
        print('PASS: selected memory evidence is unchanged; meaning, completeness, and external state are not verified')
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
