"""A modified skill or artifact cannot reuse the prior passing release evidence."""
import copy
import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from scripts.check_behavioral_evidence import REQUIRED, hashes, validate


class BehavioralEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.skill = self.root / 'skill'
        self.skill.mkdir()
        (self.skill / 'SKILL.md').write_text('Original workflow', encoding='utf-8')
        self.artifact = self.root / 'output.py'
        self.artifact.write_text('VALUE = 1\n', encoding='utf-8')
        self.evidence = {'schema_version': 1, 'skill_sha256': hashes(self.skill),
                         'runs': [{'id': name, 'host': 'fixture-host', 'task': 'bounded task',
                                   'observations': 'Fixture record only', 'fresh_context': True,
                                   'result': 'passed', 'artifacts': {'output.py': hashlib.sha256(self.artifact.read_bytes()).hexdigest()},
                                   'checks': [{'command': 'native check', 'result': 'passed', 'exit_code': 0}]}
                                  for name in sorted(REQUIRED)],
                         'limitations': ['Synthetic records test validation, not instruction following']}

    def test_current_records_are_accepted(self):
        self.assertEqual(validate(self.root, self.skill, self.evidence), [])

    def test_removing_loop_invalidates_existing_evidence(self):
        (self.skill / 'SKILL.md').write_text('Do the task.', encoding='utf-8')
        self.assertTrue(any('Skill changed' in error for error in validate(self.root, self.skill, self.evidence)))

    def test_missing_or_changed_artifacts_are_rejected(self):
        self.artifact.write_text('VALUE = 2\n', encoding='utf-8')
        self.assertTrue(validate(self.root, self.skill, self.evidence))
        self.artifact.unlink()
        self.assertTrue(validate(self.root, self.skill, self.evidence))

    def test_incomplete_failed_and_escaping_records_are_rejected(self):
        for change in ('missing', 'failed', 'same-context', 'escaping', 'bad-check'):
            with self.subTest(change=change):
                altered = copy.deepcopy(self.evidence)
                if change == 'missing':
                    altered['runs'].pop()
                elif change == 'failed':
                    altered['runs'][0]['result'] = 'blocked'
                elif change == 'same-context':
                    altered['runs'][0]['fresh_context'] = False
                elif change == 'escaping':
                    altered['runs'][0]['artifacts'] = {'../private': '0' * 64}
                else:
                    altered['runs'][0]['checks'][0]['exit_code'] = 1
                self.assertTrue(validate(self.root, self.skill, altered))

    def test_git_windows_style_checkout_keeps_fingerprinted_bytes(self):
        (self.skill / 'SKILL.md').write_bytes(b'Understand\nBuild\nVerify\nLearn\n')
        attributes = Path(__file__).resolve().parents[1] / '.gitattributes'
        if attributes.exists():
            shutil.copy2(attributes, self.root / '.gitattributes')
        expected = hashes(self.skill)
        for args in [('init', '-q'), ('-c', 'core.autocrlf=true', 'add', '.')]:
            subprocess.run(['git', '-C', str(self.root), *args], check=True, capture_output=True)
        checkout = self.root / 'checkout'
        checkout.mkdir()
        subprocess.run(['git', '-C', str(self.root), '-c', 'core.autocrlf=true', 'checkout-index',
                        '--all', '--prefix=' + checkout.as_posix() + '/'], check=True, capture_output=True)
        self.assertEqual(hashes(checkout / 'skill'), expected)


if __name__ == '__main__':
    unittest.main()
