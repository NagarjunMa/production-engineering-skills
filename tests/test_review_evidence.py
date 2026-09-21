"""Black-box checks for review provenance on real temporary Git repositories."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).resolve().parents[1] / 'skills/production-engineering-loop/scripts/review_evidence.py'


class ReviewEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        self.packet = Path(self.temp.name) / 'packet.json'
        self.git('init', '-q')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'user.name', 'Fixture')
        self.write('contract.md', 'Preserve configured bounds and credential isolation.\n')
        self.write('app.py', 'LIMIT = 10\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'base')
        self.base = self.git('rev-parse', 'HEAD').strip()

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], text=True)

    def write(self, path, content):
        dest = self.root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content)

    def run_cli(self, *args, expected=0):
        result = subprocess.run([sys.executable, str(HELPER), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def capture(self, *extra):
        self.packet.unlink(missing_ok=True)
        self.run_cli('capture', '--repo', str(self.root), '--base', self.base,
                     '--contract', 'contract.md', '--output', str(self.packet), *extra)
        return json.loads(self.packet.read_text())

    def check(self, expected=0):
        return self.run_cli('check', '--repo', str(self.root), '--packet', str(self.packet), expected=expected)

    def report(self, packet):
        return {'schema_version': 1, 'snapshot_id': packet['snapshot_id'],
                'reviewer': {'identity': 'fixture-reviewer', 'model': 'model-a',
                             'implementer_model': 'model-a', 'fresh_context': True,
                             'kind': 'fresh-context'},
                'verdict': 'no_material_findings', 'coverage': ['app.py and callers'],
                'limitations': [], 'checks': [{'id': 'C1', 'command': 'python -m unittest',
                    'result': 'passed', 'required': True, 'snapshot_id': packet['snapshot_id'],
                    'evidence': 'local log: 2 passed'}], 'findings': []}

    def validate(self, report, expected=0):
        path = Path(self.temp.name) / 'report.json'
        path.write_text(json.dumps(report))
        return self.run_cli('validate', '--repo', str(self.root), '--packet', str(self.packet),
                            '--report', str(path), expected=expected)

    def test_committed_and_dirty_snapshots(self):
        p = self.capture()
        self.assertEqual(p['head'], self.base)
        self.assertEqual(p['merge_base'], self.base)
        self.check()
        self.write('app.py', 'LIMIT = 20\n')
        self.check(expected=1)
        dirty = self.capture()
        self.assertNotEqual(p['snapshot_id'], dirty['snapshot_id'])
        self.check()

    def test_untracked_deleted_renamed_and_dependency_changes_are_stale(self):
        for action in ('untracked', 'deleted', 'renamed', 'dependency'):
            with self.subTest(action=action):
                self.git('reset', '--hard', self.base)
                self.git('clean', '-fdq')
                self.capture()
                if action == 'untracked':
                    name = 'new_file.py' if os.name == 'nt' else 'new file\nwith newline.py'
                    self.write(name, 'new code')
                elif action == 'deleted':
                    (self.root / 'app.py').unlink()
                elif action == 'renamed':
                    (self.root / 'app.py').rename(self.root / 'renamed.py')
                else:
                    self.write('requirements.txt', 'some-package==1\n')
                self.check(expected=1)

    def test_index_change_even_when_worktree_restored(self):
        self.capture()
        self.write('app.py', 'LIMIT = 30\n')
        self.git('add', 'app.py')
        self.write('app.py', 'LIMIT = 10\n')
        self.check(expected=1)

    def test_contract_and_exclusions(self):
        self.write('records/old.md', 'historical')
        self.capture('--exclude', 'records')
        self.write('records/result.md', 'current')
        self.check()
        self.write('contract.md', 'Changed requirement')
        self.check(expected=1)
        self.run_cli('capture', '--repo', str(self.root), '--contract', 'contract.md',
                     '--exclude', 'contract.md', '--output', str(self.packet), expected=2)

    def test_output_cannot_be_part_of_snapshot_or_overwrite_source(self):
        original = (self.root / 'app.py').read_text()
        self.run_cli('capture', '--repo', str(self.root), '--contract', 'contract.md',
                     '--output', str(self.root / 'app.py'), expected=2)
        self.assertEqual((self.root / 'app.py').read_text(), original)

    def test_capture_never_emits_source_or_environment_values(self):
        self.write('secret.txt', 'UNIQUE_PRIVATE_VALUE_0198')
        self.capture()
        self.assertNotIn('UNIQUE_PRIVATE_VALUE_0198', self.packet.read_text())

    @unittest.skipIf(os.name == 'nt', 'POSIX executable fsmonitor probe')
    def test_repository_fsmonitor_is_not_executed(self):
        marker = Path(self.temp.name) / 'executed'
        hook = Path(self.temp.name) / 'fsmonitor'
        hook.write_text('#!/bin/sh\ntouch "' + str(marker) + '"\n')
        hook.chmod(0o755)
        self.git('config', 'core.fsmonitor', str(hook))
        packet = self.capture()
        self.check()
        self.validate(self.report(packet))
        self.assertFalse(marker.exists(), 'Capture executed a repository-configured hook')

    @unittest.skipIf(os.name == 'nt', 'POSIX executable remote-helper probe')
    def test_missing_promised_object_never_executes_remote_helper(self):
        self.write('second.py', 'VALUE = 2\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'second')
        packet = self.capture()
        report_path = Path(self.temp.name) / 'report.json'
        report_path.write_text(json.dumps(self.report(packet)))

        marker = Path(self.temp.name) / 'remote-helper-executed'
        helper = Path(self.temp.name) / 'remote-helper'
        helper.write_text('#!/bin/sh\ntouch "' + str(marker) + '"\nexit 1\n')
        helper.chmod(0o755)
        self.git('config', 'remote.origin.url', 'ext::' + str(helper))
        self.git('config', 'remote.origin.promisor', 'true')
        self.git('config', 'protocol.ext.allow', 'always')

        git_dir = Path(self.git('rev-parse', '--git-dir').strip())
        if not git_dir.is_absolute():
            git_dir = self.root / git_dir
        base_object = git_dir / 'objects' / self.base[:2] / self.base[2:]
        self.assertTrue(base_object.is_file(), 'Fixture requires a loose base commit object')
        base_object.unlink()

        missing_output = Path(self.temp.name) / 'missing-object-packet.json'
        commands = [
            ('capture', '--repo', str(self.root), '--base', self.base,
             '--contract', 'contract.md', '--output', str(missing_output)),
            ('check', '--repo', str(self.root), '--packet', str(self.packet)),
            ('validate', '--repo', str(self.root), '--packet', str(self.packet),
             '--report', str(report_path)),
        ]
        for command in commands:
            with self.subTest(command=command[0]):
                marker.unlink(missing_ok=True)
                self.run_cli(*command, expected=2)
                self.assertFalse(marker.exists(),
                                 'Offline evidence command executed a remote helper')

    @unittest.skipIf(os.name == 'nt', 'Symlink creation may require elevated Windows privileges')
    def test_symlink_does_not_read_external_target(self):
        outside = Path(self.temp.name) / 'outside'
        outside.write_text('outside secret')
        (self.root / 'linked').symlink_to(outside)
        p = self.capture()
        self.assertEqual(p['files']['linked']['kind'], 'symlink')
        outside.write_text('changed external dependency')
        self.check()  # External contents explicitly outside the snapshot guarantee.
        self.assertTrue(p['limitations'])

    def test_unborn_repository(self):
        other = self.root / 'nested'
        other.mkdir()
        subprocess.run(['git', 'init', '-q', str(other)], check=True)
        (other / 'contract.md').write_text('new project')
        self.run_cli('capture', '--repo', str(other), '--contract', 'contract.md',
                     '--output', str(self.packet))
        p = json.loads(self.packet.read_text())
        self.assertIsNone(p['head'])
        self.run_cli('check', '--repo', str(other), '--packet', str(self.packet))

    def test_invalid_base_and_path_escape(self):
        self.run_cli('capture', '--repo', str(self.root), '--base', 'missing-ref',
                     '--contract', 'contract.md', '--output', str(self.packet), expected=2)
        self.run_cli('capture', '--repo', str(self.root), '--contract', '../secret',
                     '--output', str(self.packet), expected=2)

    def test_packet_integrity_and_stale_report(self):
        p = self.capture()
        report = self.report(p)
        self.validate(report)
        p['files']['app.py']['sha256'] = '0' * 64
        self.packet.write_text(json.dumps(p))
        self.check(expected=2)
        p = self.capture()
        report['snapshot_id'] = 'f' * 64
        self.validate(report, expected=1)

    def test_no_ready_verdict_with_failed_required_check(self):
        report = self.report(self.capture())
        for result in ('failed', 'blocked', 'not_run', 'skipped'):
            report['checks'][0]['result'] = result
            self.validate(report, expected=1)

    def test_finding_requires_evidence_and_passing_current_resolution(self):
        p = self.capture()
        report = self.report(p)
        finding = {'id': 'F1', 'severity': 'medium', 'material': True,
                   'classification': 'confirmed', 'origin': 'introduced',
                   'status': 'resolved', 'location': 'app.py:1', 'claim': 'Limit lost',
                   'criterion': 'Configured bounds', 'evidence': 'Subprocess accepts 20 with limit 10',
                   'reproducer': 'python tests/test_worker.py', 'resolution': 'Propagate validated limit',
                   'resolved_snapshot_id': p['snapshot_id'], 'check_ids': ['C1']}
        report['findings'] = [finding]
        self.validate(report)
        for field, bad in [('check_ids', []), ('resolved_snapshot_id', 'old'),
                           ('evidence', ''), ('status', 'open')]:
            altered = copy.deepcopy(report)
            altered['findings'][0][field] = bad
            self.validate(altered, expected=1)

    def test_mixed_findings_and_model_claims(self):
        p = self.capture()
        report = self.report(p)
        report['findings'] = [{'id': 'F2', 'severity': 'low', 'material': False,
            'classification': 'unsupported', 'origin': 'unknown', 'status': 'dismissed',
            'location': 'app.py:1', 'claim': 'Must use a class', 'criterion': 'None',
            'evidence': 'Contract permits functions; no state lifecycle',
            'reproducer': 'N/A: design suggestion', 'resolution': 'Retain function',
            'check_ids': []}]
        self.validate(report)
        report['reviewer']['kind'] = 'cross-model'
        self.validate(report, expected=1)
        report['reviewer']['model'] = 'model-b'
        self.validate(report)
        report['reviewer']['fresh_context'] = False
        self.validate(report, expected=1)

    def test_malformed_report_returns_errors_not_traceback(self):
        self.capture()
        for report in ([], {'schema_version': 1}, {'findings': [None]}):
            result = self.validate(report, expected=1)
            self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
