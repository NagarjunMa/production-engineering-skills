"""A failure or setup error is never scored as an expected defect detection."""
import subprocess
import sys
import tempfile
import unittest

from scripts.run_evaluations import run_case


class ReplayRunnerTests(unittest.TestCase):
    def test_positive_and_expected_negative_results(self):
        with tempfile.TemporaryDirectory() as root:
            positive = run_case('positive', [sys.executable, '-c', 'print("observed")'], root, 0, 'observed')
            negative = run_case('negative', [sys.executable, '-c',
                                'raise AssertionError("intended defect")'], root, 1, 'intended defect')
            self.assertEqual(positive['result'], 'passed')
            self.assertEqual(negative['result'], 'passed')

    def test_missing_import_is_not_the_intended_failure(self):
        with tempfile.TemporaryDirectory() as root:
            result = run_case('wrong failure', [sys.executable, '-c',
                              'import unavailable_pel_fixture_module'], root, 1, 'intended defect')
            self.assertEqual(result['result'], 'failed')

    def test_command_that_cannot_start_is_blocked(self):
        with tempfile.TemporaryDirectory() as root:
            result = run_case('unavailable', ['missing-pel-executable'], root, 1, 'defect')
            self.assertEqual(result['result'], 'blocked')


if __name__ == '__main__':
    unittest.main()
