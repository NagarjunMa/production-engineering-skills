# Session-b validation receipt

Workspace `<evaluation>/session-b` (host resolves `/private/tmp/...`),
2026-10-26, Python 3.11.1. No Git repository; `git status --short` returned 128.
Model identity unknown. Local/standard-library tools only; no network, installs,
commits, deployment, delegation or edits outside this workspace.

Checks executed in order:

1. **Passed**, exit 0, baseline 4 methods:
   `python3 -B -m unittest discover -s tests -v`.
2. **Failed as intended**, exit 1, after runnable `return {}` scaffold and 6 new
   test methods: same native command, 10 methods, 7 assertion failures. Failures
   were missing KeyError/ValueError or wrong results; empty case and original 4
   methods passed. No import/environment failure was used as behavioral evidence.
3. **Passed**, exit 0 after implementation: same native command, 10 methods,
   `Ran 10 tests in 0.000s`, `OK`. Python source/tests were unchanged afterward.
4. **Passed**, manual self-review: read entire stock.py, tests/test_inventory.py,
   README, PROJECT and feature record; searched all Python consumers with exact
   command `rg -n 'adjust_stock|adjust_many|stock\[' --glob '*.py' .`.
   One canonical validation rule; caller-owned mapping updated only after all
   candidates succeed. Repeats use tentative quantities; input list is read-only.
   No material in-scope finding observed. This is not independent review.
5. **Passed**, exit 0, exact source preservation and in-memory compilation check:

```sh
python3 -B - <<'PY_CHECK'
import hashlib
import json
from pathlib import Path

original = json.loads(Path('docs/engineering-loop/evidence/snapshot.json').read_text())['files']['inventory.py']
current_single = Path('stock.py').read_text().split('\n\ndef adjust_many')[0].rstrip() + '\n'
assert hashlib.sha256(current_single.encode()).hexdigest() == original
for path in (Path('stock.py'), Path('tests/test_inventory.py')):
    compile(path.read_bytes(), str(path), 'exec')
print('PASS: adjust_stock bytes match inherited function hash; both Python files compile in memory')
PY_CHECK
```

Historical receipts were retained, not relabeled as current. An initial apply_patch
containing delete/add operations for the same feature path was rejected before
any files changed; corrected edits succeeded. No check was skipped or weakened.

Fresh review: **blocked/pending**, explicit task restriction prohibits delegation;
portable handoff in `review-packet-b.md`. No configured lint/type/CI check exists.
External consumers, invalid types/dictionaries, concurrency and deployment were
not tested. Implementation stages a whole shallow stock copy (O(stock size) memory);
no performance improvement is claimed. Final hashes/timestamp: `snapshot-b.json`.
