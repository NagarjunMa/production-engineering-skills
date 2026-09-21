#!/usr/bin/env python3
"""Capture Git/worktree provenance and validate review records; never judge code quality.

Python 3.10+, Git. No network, shell, source execution, or third-party dependencies.
Exit 0: valid/current; 1: stale/report invalid; 2: input or capture failure.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
                                    separators=(',', ':')).encode()).hexdigest()


def git(root, *args, optional=False):
    # Keep inventory offline. Missing promised objects must fail instead of
    # fetching through a repository-configured remote or protocol helper.
    git_env = os.environ.copy()
    git_env.update({
        'GIT_ALLOW_PROTOCOL': '',
        'GIT_NO_LAZY_FETCH': '1',
        'GIT_OPTIONAL_LOCKS': '0',
        'GIT_TERMINAL_PROMPT': '0',
    })
    result = subprocess.run(['git', '-c', 'core.fsmonitor=false', '-C', str(root), *args],
                            capture_output=True, env=git_env)
    if result.returncode and not optional:
        raise ValueError('Git could not resolve repository/index/revision: ' + args[0])
    return result.stdout if result.returncode == 0 else None


def relative_path(value):
    if not isinstance(value, str) or not value or '\\' in value:
        raise ValueError('Paths must be nonempty repository-relative POSIX paths')
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts or value in ('.', './'):
        raise ValueError('Path must stay inside the repository')
    if '.git' in path.parts:
        raise ValueError('Git metadata cannot be a source or exclusion path')
    return path.as_posix()


def excluded(path, exclusions):
    return any(path == item or path.startswith(item + '/') for item in exclusions)


def revision(root, ref):
    return git(root, 'rev-parse', '--verify', '--end-of-options', ref + '^{commit}').decode().strip()


def fingerprint(root, path):
    full = root / path
    # Parent symlinks must not escape the repository, even for a tracked missing path.
    if not full.parent.resolve().is_relative_to(root):
        raise ValueError('Source parent escapes repository: ' + path)
    try:
        mode = full.lstat().st_mode
    except FileNotFoundError:
        return {'kind': 'missing'}
    if stat.S_ISLNK(mode):
        return {'kind': 'symlink', 'sha256': hashlib.sha256(os.fsencode(os.readlink(full))).hexdigest()}
    if not stat.S_ISREG(mode):
        raise ValueError('Unsupported source type (including submodule): ' + path)
    hasher = hashlib.sha256()
    with full.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            hasher.update(block)
    return {'kind': 'file', 'sha256': hasher.hexdigest(), 'executable': bool(mode & stat.S_IXUSR)}


def collect(root, base, contract, exclusions):
    head_raw = git(root, 'rev-parse', '--verify', 'HEAD', optional=True)
    head = head_raw.decode().strip() if head_raw else None
    base_id = revision(root, base) if base else None
    merge_base = git(root, 'merge-base', head, base_id).decode().strip() if head and base_id else None
    index = []
    paths = set()
    for record in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        meta, raw_path = record.split(b'\t', 1)
        path = os.fsdecode(raw_path)
        if excluded(path, exclusions):
            continue
        mode, blob, stage = meta.decode().split()
        if mode == '160000' or stage != '0':
            raise ValueError('Submodules/unmerged index need separate review evidence: ' + path)
        paths.add(path)
        index.append([path, mode, blob])
    paths.update(os.fsdecode(p) for p in git(root, 'ls-files', '--others', '--exclude-standard', '-z').split(b'\0')
                 if p and not excluded(os.fsdecode(p), exclusions))
    paths.add(contract)  # Explicitly include the contract even if ignored.
    files = {p: fingerprint(root, p) for p in sorted(paths)}
    if files[contract]['kind'] != 'file':
        raise ValueError('Contract must be an existing regular file')
    limitations = ['Ignored files, external dependencies, runtime environment, and external symlink contents are not captured.']
    if not base_id:
        limitations.append('No base supplied; origin of findings cannot be inferred from this packet.')
    if any(f['kind'] == 'symlink' for f in files.values()):
        limitations.append('Symlink targets are hashed as link text only; inspect external consumers separately.')
    return {'schema_version': 1, 'head': head, 'base': base_id, 'merge_base': merge_base,
            'contract': contract, 'exclusions': exclusions, 'files': files,
            'index': sorted(index), 'limitations': limitations}


def snapshot(root, base, contract, exclusions):
    # Refuse a changing snapshot instead of presenting a mixed read as reproducible.
    first = collect(root, base, contract, exclusions)
    second = collect(root, base, contract, exclusions)
    if first != second:
        raise ValueError('Repository changed during capture; pause writers and retry')
    return dict(first, snapshot_id=digest(first))


def load_packet(path):
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        raise ValueError('Unsupported packet schema')
    expected = data.get('snapshot_id')
    body = {k: v for k, v in data.items() if k != 'snapshot_id'}
    if expected != digest(body):
        raise ValueError('Packet integrity mismatch')
    relative_path(data['contract'])
    if not isinstance(data['exclusions'], list):
        raise ValueError('Exclusions must be a list')
    for item in data['exclusions']:
        relative_path(item)
    if excluded(data['contract'], data['exclusions']):
        raise ValueError('Contract cannot be excluded')
    if not isinstance(data['files'], dict):
        raise ValueError('Packet files must be a mapping')
    return data


def freshness(root, packet):
    current = snapshot(root, packet['base'], packet['contract'], packet['exclusions'])
    if current['snapshot_id'] == packet['snapshot_id']:
        return []
    changes = [p for p in sorted(set(current['files']) | set(packet['files']))
               if current['files'].get(p) != packet['files'].get(p)]
    return ['Review evidence is stale; capture and review the current source.',
            'Changed paths: ' + json.dumps(changes),
            'HEAD/index/base metadata changed: ' + str(any(current[k] != packet[k]
                for k in ('head', 'base', 'merge_base', 'index')))]


def validate_report(report, packet):
    """Validate evidence structure and consistency, never the truth of supplied claims."""
    errors = []
    if not isinstance(report, dict):
        return ['Report must be an object']
    def need(condition, message):
        if not condition:
            errors.append(message)
    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())
    sid = packet['snapshot_id']
    need(report.get('schema_version') == 1, 'Unsupported report schema')
    need(report.get('snapshot_id') == sid, 'Report snapshot differs from packet')
    verdict = report.get('verdict')
    need(verdict in ('no_material_findings', 'changes_required', 'blocked'), 'Invalid verdict')
    reviewer = report.get('reviewer')
    if not isinstance(reviewer, dict):
        errors.append('Reviewer metadata required')
    else:
        kind = reviewer.get('kind')
        need(kind in ('self-review', 'fresh-context', 'cross-model', 'external'), 'Invalid reviewer kind')
        need(nonempty(reviewer.get('identity')), 'Reviewer identity required')
        need(type(reviewer.get('fresh_context')) is bool, 'fresh_context must be boolean')
        if kind in ('fresh-context', 'cross-model'):
            need(reviewer.get('fresh_context') is True, 'Fresh-context claim lacks fresh context')
        if kind == 'cross-model':
            need(nonempty(reviewer.get('model')) and nonempty(reviewer.get('implementer_model'))
                 and reviewer.get('model') != reviewer.get('implementer_model'),
                 'Cross-model review requires distinct known model identities')
    for field in ('coverage', 'limitations', 'checks', 'findings'):
        need(isinstance(report.get(field), list), field + ' must be a list')
    if errors:
        return errors
    need(bool(report['coverage']) and all(nonempty(x) for x in report['coverage']), 'Record actual review coverage')
    need(all(nonempty(x) for x in report['limitations']), 'Invalid limitation')
    checks = {}
    for check in report['checks']:
        if not isinstance(check, dict):
            errors.append('Check must be an object')
            continue
        cid = check.get('id')
        if not nonempty(cid):
            errors.append('Check ID required')
            continue
        need(cid not in checks, 'Duplicate check ID: ' + cid)
        checks[cid] = check
        need(nonempty(check.get('command')) and nonempty(check.get('evidence')), 'Check command/procedure and evidence required')
        need(check.get('result') in ('passed', 'failed', 'blocked', 'not_run', 'skipped'), 'Invalid check result')
        need(type(check.get('required')) is bool, 'Check required flag must be boolean')
        need(check.get('snapshot_id') == sid, 'Check is not tied to current snapshot')
        if verdict == 'no_material_findings' and check.get('required'):
            need(check.get('result') == 'passed', 'Required check has not passed')
    ids = set()
    for finding in report['findings']:
        if not isinstance(finding, dict):
            errors.append('Finding must be an object')
            continue
        fid = finding.get('id')
        if not nonempty(fid):
            errors.append('Finding ID required')
            continue
        need(fid not in ids, 'Duplicate finding ID: ' + fid)
        ids.add(fid)
        for field in ('location', 'claim', 'criterion', 'evidence', 'reproducer'):
            need(nonempty(finding.get(field)), fid + ': missing ' + field)
        cls, status = finding.get('classification'), finding.get('status')
        need(cls in ('confirmed', 'unsupported', 'ambiguous', 'pre-existing'), fid + ': invalid classification')
        need(finding.get('origin') in ('introduced', 'pre-existing', 'unknown'), fid + ': invalid origin')
        if cls == 'pre-existing':
            need(finding.get('origin') == 'pre-existing', fid + ': pre-existing classification needs baseline origin')
        need(finding.get('severity') in ('critical', 'high', 'medium', 'low'), fid + ': invalid severity')
        need(type(finding.get('material')) is bool, fid + ': material must be boolean')
        need(status in ('open', 'resolved', 'dismissed', 'deferred'), fid + ': invalid status')
        if cls == 'unsupported':
            need(status == 'dismissed' and nonempty(finding.get('resolution')), fid + ': unsupported finding needs evidenced dismissal')
        if cls == 'ambiguous':
            need(status in ('open', 'deferred'), fid + ': resolve ambiguity before closing')
        if cls in ('confirmed', 'pre-existing'):
            need(status != 'dismissed', fid + ': supported finding cannot be dismissed')
        if verdict == 'no_material_findings' and finding.get('material'):
            need(status in ('resolved', 'dismissed'), fid + ': unresolved material finding')
        if status == 'resolved':
            need(nonempty(finding.get('resolution')), fid + ': resolution evidence required')
            need(finding.get('resolved_snapshot_id') == sid, fid + ': resolution snapshot is stale')
            cids = finding.get('check_ids')
            if not isinstance(cids, list) or not cids or not all(nonempty(c) for c in cids):
                errors.append(fid + ': resolution must reference verification checks')
            else:
                need(all(c in checks and checks[c].get('result') == 'passed'
                         and checks[c].get('snapshot_id') == sid for c in cids),
                     fid + ': resolution checks must pass on current snapshot')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='action', required=True)
    capture = commands.add_parser('capture', help='Capture source fingerprints, not source contents')
    capture.add_argument('--base', help='Verified intended integration target/ref; omitted for unknown/unborn base')
    capture.add_argument('--contract', required=True, help='Repository-relative requirements document')
    capture.add_argument('--exclude', action='append', default=[], help='Exact path/directory prefix; no glob')
    capture.add_argument('--output', type=Path, required=True, help='New output file outside repo or in explicit exclusion')
    check = commands.add_parser('check', help='Check packet integrity and current source freshness')
    validate = commands.add_parser('validate', help='Check report structure and freshness; not code quality')
    for command in (capture, check, validate):
        command.add_argument('--repo', type=Path, required=True)
    for command in (check, validate):
        command.add_argument('--packet', type=Path, required=True)
    validate.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    try:
        root = args.repo.resolve()
        discovered = Path(os.fsdecode(git(root, 'rev-parse', '--show-toplevel')).strip()).resolve()
        if root != discovered:
            raise ValueError('--repo must name the repository root')
        if args.action == 'capture':
            contract = relative_path(args.contract)
            exclusions = sorted(set(relative_path(p) for p in args.exclude))
            if excluded(contract, exclusions):
                raise ValueError('Contract cannot be excluded')
            output = args.output.resolve()
            if output.is_relative_to(root) and not excluded(output.relative_to(root).as_posix(), exclusions):
                raise ValueError('Output must be outside source snapshot or explicitly excluded')
            packet = snapshot(root, args.base, contract, exclusions)
            # Exclusive creation prevents accidental overwrite of any existing artifact/source.
            with output.open('x', encoding='utf-8') as dest:
                json.dump(packet, dest, indent=2, ensure_ascii=True)
                dest.write('\n')
            print('Captured ' + packet['snapshot_id'] + '; ' + str(len(packet['files'])) + ' paths')
            return 0
        packet = load_packet(args.packet)
        errors = freshness(root, packet)
        if args.action == 'validate':
            errors += validate_report(json.loads(args.report.read_text()), packet)
        if errors:
            print('\n'.join(errors), file=sys.stderr)
            return 1
        print('PASS: provenance' + (' and report structure; reported claims are not independently verified' if args.action == 'validate' else ' is current'))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
