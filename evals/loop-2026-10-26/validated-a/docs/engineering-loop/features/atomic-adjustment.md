# Atomic stock adjustments

## Contract and execution context

- Requirement: [README](../../../README.md); satisfy its complete stock contract.
- Scope: integer deltas, valid dictionaries, existing public signature/error types.
  No extra validation, dependencies, network, commits, deployment, or agents.
- Significant risk: public library state mutation. Compact documentation explicitly
  requested; retain full applicable checks and a pending independent-review handoff.
- Verified: `inventory.py::adjust_stock` (edit, canonical mutation rule),
  `tests/test_inventory.py::StockTests` (tests and sole discovered local caller),
  `README.md` (read, authoritative behavior).
- Initial snapshot: 2026-10-26, no project-local Git metadata. Three original files
  inspected; existing implementation mutates before validation.
- Status: implemented locally; native behavioral checks passed. Next incomplete
  step: required fresh independent review, unavailable under the no-agents limit.

## Design and acceptance

Keep one cohesive function: calculate candidate quantity, reject if negative,
then store and return it. Ordinary dictionary lookup retains `KeyError` for
unknown products. The caller owns the dictionary; no copying/replacement is
needed. There are no other production rules to consolidate, layers to introduce,
or external execution boundaries to test.

| ID | Expected behavior / forbidden effect | Test and plausible wrong implementation rejected |
| --- | --- | --- |
| A1 | Positive, zero, negative adjustments return AND store the result; zero stock is valid; other products survive | Success table checks return and entire dictionary. Rejects returning without storing, ignoring negative deltas, rejecting zero, or replacing other entries. |
| A2 | Negative result raises `ValueError`, leaving the ENTIRE dictionary unchanged | Negative cases from positive and zero stock compare pre/post snapshots. Rejects mutation before validation and clamping. |
| A3 | Unknown SKU raises `KeyError`, without inserting it or changing any entry | Missing-key cases on populated and empty dictionaries compare snapshots. Rejects default-zero insertion. |

Validation mode: behavioral red/green using the README's native command,
`python3 -B -m unittest discover -s tests -v`, from the project root. No
formatter/linter/type/CI checks are configured. Python runtime and final source
hashes are recorded in `../evidence.json`; substantive records precede capture.

## Outcome and review handoff

Changed `inventory.py` to validate the candidate before its only write; expanded
`tests/test_inventory.py` to three tests covering 14 input cases. Created this
record, `../PROJECT.md`, and the evidence receipt; README unchanged. Compatibility:
retain signature, successful mutations, error types, and `Negative stock` message;
only forbidden mutation on rejection changes. No stored-data migration or rollout
is required. Reverting the source edit would restore the known mutation defect.

Fresh independent review is required by the skill for Significant work but is
pending: further agents are prohibited by the task. Self-review completed as self-review; model identity is unknown. It does not
satisfy required independent review. Reviewer rounds: 0 of 3.

Portable reviewer task: review only this project, using the README and A1–A3 above;
inspect the function, callers/tests, entire final manifest, and error paths;
independently run the native command without changing sources or contacting
external services. Check `../evidence.json` hashes before and after review.
Base/branch/merge base and external consumers are unknown. Report actual reviewer
identity/model (unknown if unavailable), context independence, snapshot, commands,
coverage, and location-backed findings or no findings. Return the report inline;
do not spawn reviewers, commit, deploy, or edit project records. Historical test
results below are implementer observations, not independent review evidence.

## Local evidence and retained lesson

- Baseline native command: **passed**, one existing success test.
- Expanded tests before fix: **failed**, two negative-result subcases retained
  `-1` in the dictionary; all success and missing-product cases passed. This is
  the intended behavioral red state, not a collection failure.
- Same native command after fix: **passed**, 3 tests, 14 subcases (2026-10-26).
  A1–A3 are covered. No other repository gates are configured; hosted checks and
  independent review were **not run**. Required independent review remains pending.
- Self-review: read the complete function, test consumers and README; confirmed
  missing-key lookup happens before mutation, the negative branch has no writes,
  zero is accepted, success has one write to the existing SKU, and the return is
  the stored quantity. No duplicate rule, dependency, or unrelated behavior added.
- Finding INV-1: confirmed, pre-existing, medium severity; original
  `inventory.py::adjust_stock` wrote before checking for negative stock. Resolved
  by candidate validation before assignment; the full-dictionary regression and
  final native command pass. No known material code finding remains.
- Scoped lesson: for this caller-owned dictionary API, testing only the raised
  error misses forbidden state changes. Check the entire dictionary against its
  pre-call copy on both negative-result and unknown-product rejection.
- Release status: no release requested/performed. Local behavior verified;
  overall review readiness remains pending. No performance claim or exhaustive
  guarantee; external consumers and out-of-scope input types remain unverified.
