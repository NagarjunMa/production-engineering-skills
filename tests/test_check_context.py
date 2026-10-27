"""Memory receipts track selected evidence without requiring Git or editing it."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).resolve().parents[1] / 'skills/production-engineering-loop/scripts/check_context.py'


class ContextTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / 'project'
        self.root.mkdir()
        (self.root / 'PROJECT.md').write_text('The limit is in app.py.\n', encoding='utf-8')
        (self.root / 'app.py').write_text('LIMIT = 10\n', encoding='utf-8')
        self.receipt = Path(self.temporary.name) / 'context.json'

    def cli(self, *args, expected=0):
        result = subprocess.run([sys.executable, '-B', str(HELPER), *args,
                                 '--repo', str(self.root)], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        return result

    def capture(self):
        result = self.cli('capture', '--record', 'PROJECT.md', '--source', 'app.py')
        self.receipt.write_text(result.stdout, encoding='utf-8')
        return json.loads(result.stdout)

    def check(self, expected=0):
        return self.cli('check', '--receipt', str(self.receipt), expected=expected)

    def test_current_non_git_receipt_is_read_only(self):
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        self.capture()
        self.check()
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})

    def test_plain_invocation_does_not_write_into_the_installed_skill(self):
        installed = Path(self.temporary.name) / 'installed'
        installed.mkdir()
        for name in ('check_context.py', 'review_evidence.py'):
            shutil.copy2(HELPER.with_name(name), installed / name)
        before = {p.name: p.read_bytes() for p in installed.iterdir()}
        environment = {key: value for key, value in os.environ.items()
                       if key not in ('PYTHONDONTWRITEBYTECODE', 'PYTHONPYCACHEPREFIX')}
        result = subprocess.run([sys.executable, str(installed / 'check_context.py'), 'capture',
                                 '--repo', str(self.root), '--record', 'PROJECT.md', '--source', 'app.py'],
                                capture_output=True, text=True, env=environment, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        after = {p.relative_to(installed).as_posix(): p.read_bytes()
                 for p in installed.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_changed_and_missing_evidence_is_stale(self):
        for name in ('app.py', 'PROJECT.md'):
            with self.subTest(name=name):
                self.capture()
                original = (self.root / name).read_bytes()
                (self.root / name).write_text('changed\n', encoding='utf-8')
                self.assertIn(name, self.check(expected=1).stderr)
                self.capture()
                (self.root / name).unlink()
                self.assertIn(name, self.check(expected=1).stderr)
                (self.root / name).write_bytes(original)

    def test_rename_does_not_silently_refresh_memory(self):
        self.capture()
        (self.root / 'app.py').rename(self.root / 'renamed.py')
        self.check(expected=1)
        self.assertIn('app.py', (self.root / 'PROJECT.md').read_text())

    def test_escaping_or_missing_sources_are_rejected(self):
        for path in ('../outside', '/outside', '.git/config', 'missing.py'):
            with self.subTest(path=path):
                self.cli('capture', '--record', 'PROJECT.md', '--source', path, expected=2)

    def test_paths_are_canonical_and_record_is_not_its_own_evidence(self):
        packet = json.loads(self.cli('capture', '--record', './PROJECT.md',
                                     '--source', './app.py').stdout)
        self.assertEqual(set(packet['files']), {'PROJECT.md', 'app.py'})
        self.cli('capture', '--record', 'PROJECT.md', '--source', './PROJECT.md', expected=2)

    @unittest.skipIf(os.name == 'nt', 'Symlinks may require Windows elevation')
    def test_symlink_source_is_rejected_without_reading_target(self):
        outside = Path(self.temporary.name) / 'outside'
        outside.write_text('PRIVATE_SENTINEL', encoding='utf-8')
        (self.root / 'link').symlink_to(outside)
        result = self.cli('capture', '--record', 'PROJECT.md', '--source', 'link', expected=2)
        self.assertNotIn('PRIVATE_SENTINEL', result.stdout + result.stderr)

    def test_malformed_or_tampered_receipt_fails_closed(self):
        for value in ([], {}, {'schema_version': 1}, {'schema_version': 1, 'files': []}):
            self.receipt.write_text(json.dumps(value), encoding='utf-8')
            self.check(expected=2)
        packet = self.capture()
        packet['files']['app.py']['sha256'] = '0' * 64
        self.receipt.write_text(json.dumps(packet), encoding='utf-8')
        self.check(expected=2)

    def test_receipt_records_only_hashes_and_selected_paths(self):
        (self.root / 'unselected.txt').write_text('PRIVATE_SENTINEL', encoding='utf-8')
        packet = self.capture()
        self.assertEqual(set(packet['files']), {'PROJECT.md', 'app.py'})
        self.assertNotIn('PRIVATE_SENTINEL', self.receipt.read_text())


if __name__ == '__main__':
    unittest.main()
