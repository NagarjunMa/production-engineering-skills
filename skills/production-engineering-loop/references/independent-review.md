# Independent review and findings resolution

## Select the review route

Default: self-review for Trivial/local Standard work; fresh review for Significant/Critical work and Standard changes to shared rules, architecture, or execution contracts. Honor a user/project `always` preference. A requested review-only task stays read-only even when delegated. Existing repository approval requirements still apply.

Use a fresh subagent context if available. Delegate only the review; the parent owns implementation and resolution. For Codex routing see [codex-review.md](codex-review.md). Do not inherit the implementer's entire conversation or feed the reviewer a desired verdict. Supply requirements, applicable repository instructions, source access, base/current snapshot, and commands as reported history. The reviewer chooses relevant investigation, inspects callers, and independently verifies material claims. It may expand inspection beyond the packet's path hints.

If tools cannot delegate, prepare [review-packet-template.md](../assets/review-packet-template.md) and [reviewer-prompt.md](../assets/reviewer-prompt.md). Return inline artifacts when writing is outside scope. Complete safe implementation/checks and report required review pending; do not pretend the packet is a completed review.

Identify actual independence descriptively: `self-review`, `fresh-context`, `cross-model`, or `external`. A different task or agent name does not establish a different model. Use `cross-model` only for known distinct model identities and a fresh context. Unknown model identity stays unknown. Different models may share failure modes; labels are not a numerical assurance ranking.

## Capture and dispatch

1. Verify the problem statement and acceptance criteria. Name the intended integration target; do not assume `main` or `HEAD~1`. Preserve exclusions and unrelated edits.
2. Capture a stable source snapshot per [review-evidence.md](review-evidence.md). For dirty work include staged, unstaged, untracked, deleted files, and changed dependencies. Pause relevant writers during capture/review or give the reviewer an isolated copy of that snapshot. A worktree at HEAD alone omits uncommitted changes.
3. Give the reviewer the contract, packet, repository instructions, and [reviewer prompt](../assets/reviewer-prompt.md). Mark historical check results as reported, not independently reproduced. Do not include credentials, environment dumps, or implementation advocacy.
4. Run review in the current task through host delegation; no new user-visible task is necessary. The reviewer may run authorized local checks without changing source. Use isolated scratch for mutating tests and report unavailable tools. Reviewers must not launch another reviewer or recursively apply the dispatch stage.
5. Check freshness when the reviewer returns. Preserve a stale report as history; refresh or review the affected correction before using it for readiness.

## Resolve findings

Maintain stable IDs with severity, materiality, source location, claim, affected criterion, evidence, classification, origin, reproducer, disposition, resolution checks, and tested snapshot. Use the [report template](../assets/review-report-template.json) for machine validation or the same fields in an existing compact/full feature record. Read its [schema guidance](review-evidence.md) before filling it.

| Classification | Required decision/evidence |
| --- | --- |
| confirmed | Reachable failure or concrete maintenance cost supported by source/tests; fix within authorization |
| unsupported | Requirement/behavior does not support the suggestion; retain contrary evidence and dismiss, without speculative edits |
| ambiguous | Evidence conflicts or intended behavior is missing; investigate, then ask only for the unresolved decision |
| pre-existing | Verified at the actual base; record baseline evidence and whether a required gate still blocks acceptance |

Origin (`introduced`, `pre-existing`, `unknown`) is also recorded separately: a confirmed defect can have unknown origin. Do not claim pre-existing merely because the changed lines are elsewhere. If no base exists, record unknown origin.

For confirmed in-scope defects: add a meaningful failing reproducer when practical, fix the smallest coherent cause, and run the reproducer plus affected checks. Preserve characterization tests for pure refactors. For non-executable findings use a precise structural inspection with source references. Never weaken valid checks or change a criterion just to obtain a pass.

Mark resolved only with current source evidence and passing applicable checks. Mark unsupported dismissed only with evidence. Pre-existing required-gate failures remain visible and can block readiness even outside fix scope. Ambiguous material findings remain open. Re-review corrected paths and related consumers; review the full final manifest for new changes or gaps. Keep earlier reports immutable and link the final resolution ledger.

## Bound the loop and learn

Default budget: three reviewer rounds total (initial plus at most two returns); allow explicit user/project budgets. Stop earlier after two failed fixes of the same finding without new evidence, an unavailable required reviewer, or a missing material decision. Report pending work and keep other authorized progress moving. A budget limit never converts an unresolved defect into a pass. Count rounds at the coordinating agent so fresh reviewer contexts cannot reset the limit.

Before readiness: applicable required checks passed, required review completed on current code, no unresolved material finding or blocking pre-existing gate. Critical work retains required human/domain review and release authorization. Compact/full documentation changes presentation only.

After an evidenced correction, retain a reusable project lesson only with its applicability, evidence, and regression/detection check. Unsupported reviewer opinions are not project rules. Never automatically mutate the installed skill or broaden this task to implement unrelated lessons.
