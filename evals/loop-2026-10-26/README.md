# Current loop release evaluation

This protocol exercises the local v0.7 skill in fresh agent contexts. It is a
bounded engineering-workflow evaluation, not a benchmark or a guarantee for every
host. Keep an exact copy/fingerprint of the tested package with the run metadata.

## Reproduce a fresh run

1. Copy `starting/` into a disposable project. Supply the current skill and
   `task-a.txt` to a fresh agent, without evaluator expectations or earlier chat.
2. Inspect the output and run `python3 -B evals/loop-2026-10-26/verify_single.py
   /absolute/path/to/session-a` from this repository. Native tests must also pass.
   Reconstruct the original implementation with the new tests in a disposable
   copy to verify that the defect is detected.
3. Copy the completed project for session B. Rename `inventory.py` to `stock.py`
   and update only the native imports and README API location. Leave prior memory
   paths stale. Add an explicitly unverified note claiming zero stock is invalid,
   and an unrelated append-only-log lesson. Preserve the lesson from A.
4. Supply only the project, skill, and `task-b.txt` to another fresh context. Use
   `verify_stock.py` from `evals/audit-2026-09-18/` against the resulting project.
   Inspect how the agent handled old locations, prior lessons, and contrary notes.
5. In a separate copy of `review-only/`, ask a fresh agent to review `search.py`
   against README, without modifying any project files. Check the zero-limit
   finding and compare every file before and after. Use scratch for writes.

No network, secrets, new dependencies, commits, deployment, or nested delegation is
needed. Prohibited delegation means a required additional review stays pending;
never grade a fabricated independent verdict as success. A coordinator can review
the results afterward. Record that actual isolation is a writable disposable
workspace plus before/after comparison, not an enforced read-only sandbox.

## Deterministic versus live checks

`python3 scripts/run_evaluations.py` replays retained outputs and negative controls.
It does not perform the steps above or verify that a changed skill will make the
same decisions. Instruction changes need a new live run. Preserve source package
fingerprints, prompts, outputs, actual checks, and failures; do not substitute a
wording match for behavior.

The single-item evaluator uses explicit failures and works under optimized Python.
The older stock/quote/worker evaluators refuse optimization. All import fixture
code, so use only trusted isolated inputs.

## Current run

Executed 2026-10-26 with three fresh Codex subagent contexts and no inherited chat.
They used an exact copy of the current v0.7 package, local standard-library tools,
and the host's inherited model. Exact model/build identifiers were not independently
captured. Global Ponytail guidance was also active. No cross-model or cross-host
comparison is claimed.

| Scenario | Coordinator verification | Observed workflow |
| --- | --- | --- |
| A: implementation, corrected package | 3 native tests; 336 independent single-item cases passed; final tests reject original mutation bug in 2 subcases | Read contract/source, defined cases, fixed validation before mutation, retained project map and a scoped lesson in the feature record |
| B: fresh continuation, corrected package | 8 native tests; 7,380 batch cases plus 42 single-item cases passed | Reused `adjust_stock` on tentative state, corrected renamed locations, rejected unsupported zero-rejection advice, left unrelated logging lesson scoped |
| Review only | Zero-limit finding verified; complete before/after workspace comparison matched | Reported the bug and missing evidence without changing code or creating memory |

The first development run is preserved in `completed-a/`, `completed-b/`, and
`results-initial.json` (4/10 native tests; coordinator reconstructed 2/7 intended
failures). It predates the installed-cache correction and is historical evidence.
Fresh runs against the corrected exact package are retained in `validated-a/`,
`validated-b/`, and `results.json`. The coordinator reran both final suites and
independent acceptance checks and reconstructed the new A/B red conditions with
2/11 intended failures. Original tool chronology remains agent-reported; the later
reconstructions establish defect detection. These are development iterations,
not matched quality comparisons.

Initial Markdown receipts have author/workspace paths replaced with placeholders;
later fixture JSON retains temporary project paths and source hashes, not personal
home paths. Sanitized logs are reported history. Snapshots and retained source
must be interpreted with their own exclusion sets, not relabeled as a new run.

The memory checker rejected B's pre-rename receipt before the agent ran, identifying
the missing module and changed test import. This checks selected byte freshness;
the agent's actual source inspection, rather than a hash, resolved the stale facts.
Both implementations kept required fresh review pending when delegation was
prohibited. That is correct scope behavior, not an independent approval of those
fixtures. See [read-only observation](read-only-review.md) and [results](results.json).

`python3 scripts/check_behavioral_evidence.py` verifies that the current package
matches the recorded skill fingerprints, all three scenarios are recorded as
passing fresh-context runs, and retained artifacts have not changed. CI runs it.
Changing the skill requires new behavioral evidence; updating hashes alone is not
a substitute for rerunning the scenarios. This guard checks integrity/consistency,
not the truth of model identity or execution claims. Human/coordinator inspection
and actual acceptance runs remain necessary.

## Claims this cannot establish

One run cannot prove general quality improvements, reliable learning, or equivalent
behavior across coding tools. For benefit claims, compare repeated matched runs
of task alone, task plus the same memory, and task plus memory plus skill. Keep
evaluator cases unseen and assess design separately from behavior. Account for
other active instructions such as Ponytail rather than attributing all effects
to this skill.
