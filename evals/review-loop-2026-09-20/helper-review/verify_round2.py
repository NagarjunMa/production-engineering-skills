"""Verify fsmonitor isolation without writing into the caller's directory."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HELPER = Path(__file__).resolve().parents[3] / 'skills/production-engineering-loop/scripts/review_evidence.py'


def main():
    with tempfile.TemporaryDirectory(prefix='pel-fsmonitor-') as temporary:
        root = Path(temporary)
        repo = root / 'repo'
        repo.mkdir()
        for args in [('init', '-q'), ('config', 'user.email', 'probe@example.invalid'),
                     ('config', 'user.name', 'Probe')]:
            subprocess.run(['git', '-C', str(repo), *args], check=True, capture_output=True)
        (repo / 'contract.md').write_text('Protect evidence provenance.\n', encoding='utf-8')
        (repo / 'app.py').write_text('print(1)\n', encoding='utf-8')
        hook = root / 'fsmonitor.sh'
        hook.write_text('#!/bin/sh\nprintf invoked >> "$0.ran"\n', encoding='utf-8')
        hook.chmod(0o700)
        marker = root / 'fsmonitor.sh.ran'
        subprocess.run(['git', '-C', str(repo), 'config', 'core.fsmonitor', str(hook)], check=True)
        packet = root / 'packet.json'

        def run(action, *extra):
            result = subprocess.run([sys.executable, '-B', str(HELPER), action, '--repo', str(repo),
                                     *extra], capture_output=True, text=True, timeout=15)
            if result.returncode or marker.exists():
                raise SystemExit(action + ' failed isolation: ' + result.stdout + result.stderr)
            print(action + ': PASS; configured fsmonitor never executed')

        run('capture', '--contract', 'contract.md', '--output', str(packet))
        run('check', '--packet', str(packet))
        data = json.loads(packet.read_text(encoding='utf-8'))
        report = {'schema_version': 1, 'snapshot_id': data['snapshot_id'],
                  'reviewer': {'identity': 'probe', 'model': None, 'implementer_model': None,
                               'fresh_context': False, 'kind': 'self-review'},
                  'verdict': 'no_material_findings', 'coverage': ['fsmonitor regression only'],
                  'limitations': ['Synthetic report exercises validation, not an independent review'],
                  'checks': [], 'findings': []}
        report_path = root / 'report.json'
        report_path.write_text(json.dumps(report), encoding='utf-8')
        run('validate', '--packet', str(packet), '--report', str(report_path))


if __name__ == '__main__':
    main()
