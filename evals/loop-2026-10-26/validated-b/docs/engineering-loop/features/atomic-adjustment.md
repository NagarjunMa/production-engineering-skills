# Atomic stock adjustments

## Current contract and execution context

Compact mode is explicitly requested for this bounded addition. Significant risk:
a public library API mutates caller-owned state. Source of intent: README plus the
2026-10-26 task adding `adjust_many(stock, adjustments)`.

- Verified current paths: `stock.py::adjust_stock` owns the quantity/error rules;
  `tests/test_inventory.py` contains all discovered local callers. `inventory.py`
  in older records is stale after a rename; no such source exists now.
- Preserve `adjust_stock`, integer-delta/valid-dictionary scope, zero acceptance,
  error types/messages, unrelated products, and the input adjustment list.
- Batch pairs are ordered; repeated SKUs operate on tentative quantities. Reject
  intermediate underflow even if a later adjustment would repair it. Unknown SKU
  or underflow leaves the entire original dictionary unchanged. On success update
  the same dictionary and return only final touched quantities; empty input is {}.
- No I/O, concurrency, persistence, dependencies, network, commits, deployment,
  further agents, or edits outside this project are authorized.
- Implementation and local validation complete. Next incomplete step: required
  fresh independent review, prohibited in this task; portable handoff below.

## Design and acceptance evaluations

Reuse `adjust_stock` against a tentative dictionary, then commit touched values
only after the loop succeeds. This centralizes quantity/error policy and keeps
batch ordering/commit ownership in the same small module. A dictionary copy is
sufficient for integer values; no abstraction or additional validation is needed.

| ID | Criterion | Check and plausible mistake rejected |
| --- | --- | --- |
| A1 | Single adjustment stores/returns quantity, accepts zero, preserves other products | Existing success table rejects rejecting zero or returning without storing. |
| A2 | Single underflow raises ValueError without mutation | Existing whole-dictionary snapshots reject write-before-validation. |
| A3 | Single unknown SKU raises KeyError without mutation | Existing missing-key cases reject default-zero insertion. |
| B1 | Ordered batch updates original, returns final touched values only | Success tables with repeated SKUs, replenishment and zero deltas reject independent evaluation, lost repeats or returning untouched values. |
| B2 | Any unknown SKU/underflow rolls back every change | Failures after earlier valid adjustments compare entire stock and exact error arguments; reject incremental writes or error translation. |
| B3 | Intermediate underflow invalid even if final net delta is valid; first error wins | Ordered failure cases reject netting deltas or prevalidating unknown keys ahead of earlier underflow. |
| B4 | Empty batch returns {}; adjustment list preserved on success/failure | Explicit empty case and list snapshots reject mutation/consumption of caller list. |

Native gate: `python3 -B -m unittest discover -s tests -v`. No configured lint,
type, package or CI gates exist. Validation mode: behavioral red/green. Baseline
on 2026-10-26: passed, 3 tests (14 subcases), current `stock.py`.

## Prior evidence and applicability

Historical session-A evidence is retained in `../evidence.json` and
`../context-before-rename.json`; it references the old filename/location and does
not establish freshness for this task. Prior finding INV-1 was confirmed and fixed:
the original single adjustment wrote before validating negative stock. Current
source and the passing baseline preserve that fix; A2 remains its regression.
The imported claim that zero must be rejected is unsupported by the README and
current task. The append-only logging note applies to a different subsystem and
creates no requirement here.

## Review and handoff

Required fresh independent review remains pending: further agents are prohibited.
Self-review does not satisfy it. Actual reviewer/model identity is unknown;
reviewer rounds used: 0 of 3. The final receipt will be `../evidence-batch.json`.

Portable reviewer task: review only this project, read README and A1–B4, inspect
`stock.py`, all local tests and the final manifest, and independently run the native
gate without changing sources or using network/agents. Verify receipt hashes
before/after. Report actual identity/model (unknown if unavailable), independence,
coverage, checks, limits, and location-backed findings or no findings. Integration
target, branch/base, external consumers and supported Python range are unknown.
No release was requested. Removing the additive function reverts this feature;
external adoption is unknown. The intended integration target is this local project;
Git metadata is absent. Requirements and constraints above are the review contract;
source/test paths are hints, not a restriction against inspecting this project.
Historical test claims below are implementer observations, not reproduced review.
Review remains pending; do not infer acceptance from the handoff packet.


## Current results (2026-10-26)

- Baseline native gate: **passed**, 3 existing tests / 14 input cases.
- Runnable batch scaffold returning {}: **failed**, 11 behavioral failures across
  success/error cases; existing tests and empty batches passed. This was an
  intended red state, not an import/collection failure.
- Final native gate: **passed**, 8 tests / 27 input cases, A1–B4. No code/test
  changes followed that run. Static compilation of owned Python files: **passed**.
- Self-review: inspected complete source, all tests, README and project records.
  `adjust_stock` is unchanged. Batch copies integer quantities, applies the
  canonical rule in order, and writes original stock only after full success.
  Repeated touched values overwrite only the result entry. No rule duplication,
  external I/O, dependencies, unrelated behavior, or known material finding.
- Changed: `stock.py` adds the batch function; tests add five batch methods;
  README documents it; PROJECT/this record/LESSONS refresh stale context and
  retain scoped evidence; `evidence-batch.json` captures the final source.
  Existing historical receipts remain unchanged and explicitly historical.
- Limits: independent review **not run/pending**, no configured additional gates,
  external consumers/version matrix unverified. No performance claim, release,
  or guarantee about concurrency or invalid input types.
