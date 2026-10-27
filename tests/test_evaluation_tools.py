"""Evaluation commands must preserve caller files and reject disabled checks."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EvaluationSafetyTests(unittest.TestCase):
    @unittest.skipIf(os.name == 'nt', 'Historical POSIX fsmonitor reproduction')
    def test_probes_preserve_existing_caller_files(self):
        for name, folder in [('probes.py', 'probe-repo'), ('verify_round2.py', 'round2/repo')]:
            with self.subTest(script=name), tempfile.TemporaryDirectory() as temporary:
                caller = Path(temporary)
                sentinel = caller / folder / 'app.py'
                sentinel.parent.mkdir(parents=True)
                sentinel.write_text('CALLER_OWNED = True\n', encoding='utf-8')
                script = ROOT / 'evals/review-loop-2026-09-20/helper-review' / name
                result = subprocess.run([sys.executable, '-B', str(script)], cwd=caller,
                                        capture_output=True, text=True, timeout=30)
                self.assertEqual(sentinel.read_text(), 'CALLER_OWNED = True\n')
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(sorted(p.name for p in caller.iterdir()), [folder.split('/')[0]])

    def test_optimized_evaluators_fail_closed(self):
        scripts = (
            ('evals/audit-2026-09-18/verify_stock.py',
             ['evals/audit-2026-09-18/completed-fixtures/with-skill']),
            ('evals/quality-first-2026-09-18/verify_quotes.py',
             ['evals/quality-first-2026-09-18/completed-fixture']),
            ('evals/review-loop-2026-09-20/verify_outcomes.py',
             ['worker', 'evals/review-loop-2026-09-20/baseline/raw-worker-start']),
        )
        for script, arguments in scripts:
            with self.subTest(script=script):
                result = subprocess.run([sys.executable, '-B', '-O', str(ROOT / script),
                                         *arguments], cwd=ROOT, capture_output=True,
                                        text=True, timeout=10)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('optimization', result.stderr.lower())
                self.assertNotIn('PASS', result.stdout)


if __name__ == '__main__':
    unittest.main()
