# Unassigned — worker configuration

## Execution Context
Requirement sources: README.md, AGENTS.md, review-input.md. Full documentation mode because configuration crosses a credential-isolated process boundary. Critical tier conservatively covers the explicit secrets invariant.
Initial clean base: ea6e6faa98e1e02d4b8e255b5d4a4f05e92118a1, inspected 2026-09-20. Integration/release target unknown; this base is the supplied starting fixture, not an assumed branch target.
Implementation and local verification complete. Next handoff step: consult immutable candidate-evidence reports for fresh-review verdict and current snapshot freshness. No blocking product decision.
Verified locations: parent.py Tool.__init__/local/worker; policy.py normalize_text; worker.py main; adapters.py web_error/cli_error; existing tests/test_defaults.py. Implemented and verified: tests/test_worker_contract.py and shared validate_limit in policy.py. Refresh paths/source before edits on resumption; expand if additional callers emerge.

## Problem and Goal
Tool.worker serializes text only, so configured limits disappear. Match local and worker accept/reject behavior for every supported positive integer limit without transmitting parent environment data.

## Change Contract
Scope: report item 1, regression checks, associated review evidence. Item 2 conflicts with documented distinct adapter contracts; item 3 is unrelated cleanup. Retain both implementations unchanged.
Invariants: child invocation env={}, absolute Python executable, five-second timeout, value/error response shape, pre-strip Python-character length check. Legacy text-only worker requests keep default limit. Explicit invalid limits are rejected using the same positive-integer rule. No dependencies or external access.
Trust boundary: parent configuration and text -> JSON stdin -> subprocess receiver. Child environment is independently emptied. Only text and validated non-secret limit are transported.

## Design and Quality Constraints
policy.py is canonical owner of normalization and shared limit validation; parent orchestrates I/O and validates construction; worker validates decoded configuration through policy. Keep adapters independent because HTTP-style data differs from CLI exit/message semantics. No new layer or package is needed.

## Implementation and Verification Plan
Behavior change: add tests, observe non-default regression, implement transport and receiver validation, run full native gate, inspect diff, capture immutable manifest, delegate fresh review. Characterize adapter contracts before changes.

## Acceptance Criteria and Evaluations
| ID | Contract/cases | Expected and wrong implementation rejected | Check |
| --- | --- | --- | --- |
| AC1 | limits 1,5,12,20; exact and over; Unicode and whitespace | local/worker agree; limit 5 rejects six and limit 20 accepts thirteen; rejects omitted/default-only limit transport and byte-counting | worker contract tests |
| AC2 | synthetic parent credential sentinel and subprocess invocation | sentinel absent in child, parent retained, env={} and absolute executable; rejects inherited/copied environment | real subprocess plus invocation checks |
| AC3 | invalid parent/receiver limits: bool, zero, negative, float, string, null; missing receiver limit | invalid -> same error; missing -> default; rejects coercion or trust in caller-only validation | constructor and direct worker tests |
| AC4 | web and CLI error paths; unrelated legacy | (400, nested error data) versus (2, prefixed message), unchanged legacy; rejects merged shapes/unrelated rename | adapter characterization plus diff |
| AC5 | native gate and fresh review | no unresolved material finding | unittest + independent review |

## Security and Privacy
Only synthetic sentinel data used. No authentication, personal data, storage, network, deployment or package publication involved. JSON configuration gets receiver validation; credential environment is never forwarded. Runtime-added environment names may exist even with env={}.

## Compatibility, Rollout and Rollback
Parent/worker ship together in this fixture. Text-only direct worker requests retain default behavior; limit is additive. No migration or persistent data. Local-only delivery; no release is authorized. Rollback reverts parent/policy/worker changes together; this reintroduces the known non-default bug. Critical additional review is required before release claims; automated review is evidence, not permission.

## Progress and Evidence
Initial native gate: 2 tests passed on supplied raw base; historical log ../candidate-evidence/baseline.log outside repository. Regression-first result: 9 tests executed with 12 expected failed subcases before correction, then all 9 passed. See red.log and green.log; final post-capture checks will be recorded separately. Full source inspection found no other consumers. Final evidence and finding dispositions will be recorded in sibling candidate-evidence; packets identify dirty/untracked source. No TDD exception.

## Learning and Handoff
Verified lesson: default-only subprocess tests cannot detect dropped effective configuration; validate both lower and higher limits and credential isolation independently. Promote only after red/green evidence.

## Actual Changes and Dispositions
parent.py now transports limit and calls shared validation. policy.py owns positive-integer validation used by both parent and receiver normalization. worker.py consumes additive limit with legacy default. tests/test_worker_contract.py supplies real-boundary, invalid-input, Unicode, environment, and adapter cases. Project and feature memory added. adapters.py, legacy.py, README.md, AGENTS.md and incoming report remain untouched.

R1 confirmed, pre-existing at raw base: dropped limit reproduced red and corrected green. R2 unsupported: merging error shapes violates README, and distinct-contract characterization passes. R3 unsupported for this task: AGENTS limits fixes to worker report; renaming unrelated cosmetic legacy data is excluded. Structured final dispositions, snapshot IDs, independent reviewer provenance and logs live in sibling candidate-evidence.

Status: implemented and verified locally; fresh-review completion is established only by the separate report, not this pre-review record. No release performed. Unknown external consumers and runtimes beyond Python 3.11.1 remain unverified; no malformed non-text/JSON protocol redesign, resource stress tests or deployment checks were required.
