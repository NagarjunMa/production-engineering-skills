# Unassigned — Evaluation safety and memory checks

## Contract and context

User request, 2026-10-26: implement the audit fixes and missing evaluation/memory checks, verify the loop, and document only established behavior. Base: `4501e91d555222ec53873bd13c3671fb59714c5e`; branch: `codex/evaluation-memory-checks`. The starting worktree was clean.

Risk: Significant. New local validation scripts affect evidence integrity and shared skill instructions. Compact documentation follows the requested simple implementation. No new runtime dependency, background service, model provider, automatic deployment, or silent skill update is required.

## Acceptance criteria

| ID | Required behavior | Detecting check |
| --- | --- | --- |
| E1 | Historical reproduction scripts use disposable directories and preserve existing caller files | Run both from a directory containing sentinel fixtures |
| E2 | Optimized Python cannot disable acceptance checks and emit success | Run all acceptance evaluators under `-O` |
| E3 | Optional memory receipts detect changed/deleted records and selected source, reject escaping paths, and work without Git | Black-box CLI tests with temporary non-Git projects |
| E4 | A repository command replays trusted positive/negative fixture checks and reports actual outcomes separately from agent behavior | Replay runner tests and execution |
| E4b | A changed skill or retained artifact cannot reuse the current release's behavioral evidence | Behavioral-evidence guard and mutation/incomplete-record tests |
| E5 | Final review includes stable source/docs; later evidence receipts do not invalidate that source, while changed requirements do | Evidence finalization integration test |
| E6 | Current skill is forward-tested in fresh contexts for implementation, lesson reuse with stale paths, and read-only review | Isolated agent runs plus independent acceptance and file-integrity checks |
| E7 | Documentation describes current implementation and measured limits; public security channel works | Package/link checks, source review, GitHub readback |

## Plan and design

Reuse the standard-library provenance helper's path validation and fingerprint functions for an optional memory checker. Keep receipts separate from source and never execute instructions stored in memory. Replay existing deterministic evaluations in CI; keep live-agent evidence a separate release check. Preserve marketing assets and remediate their dependencies instead of deleting user work.

Finalize substantive documentation before final source capture. Store mutable final review IDs/results outside that source snapshot. Record live-agent outcomes only after inspection; fixture replay is not a quality-improvement benchmark.

## Implementation and verification

Implemented in this dirty worktree; local metadata is v0.7.0. Checks executed on
2026-10-26 with Python 3.11.1:

| Criterion | Implementation and actual evidence |
| --- | --- |
| E1 | Both historical probes now use one shared disposable implementation. Added sentinel regressions reproduced overwrites before correction and pass afterward. |
| E2 | All three assertion-based evaluators reject optimized execution. Tests with real fixture arguments initially returned false success under `-O`; corrected runs fail closed. |
| E3 | Bundled `check_context.py` reuses provenance path/fingerprint functions, supports non-Git projects, checks receipt integrity and selected evidence, rejects escaping/symlink capture inputs, and suppresses local bytecode writes. Nine black-box tests include plain-Python invocation in a clean installed copy. |
| E4 | `scripts/run_evaluations.py` runs trusted retained implementations in disposable copies, captures actual outcomes/input fingerprints, checks specific negative-control failures, and refuses receipt overwrites. All 14 fixture/control checks pass. |
| E4b | `scripts/check_behavioral_evidence.py` ties the current 27-file skill to three retained fresh-context outcomes and artifact hashes. Five tests cover stale/incomplete evidence and configured CRLF checkouts. `.gitattributes` preserves LF text and binary media. This checks consistency, not execution truth. |
| E5 | Skill/reference/templates now finalize substantive documentation before final capture and keep later IDs/results in separate evidence. Integration test accepts evidence-only writes and rejects changed requirements. |
| E6 | Three fresh Codex contexts against the corrected package exercised implementation, continuation, and read-only review. Native suites passed 3 and 8 tests; coordinator acceptance passed 336 single-item and 7,422 batch/compatibility cases and reconstructed 2/11 intended red failures. Stale paths and contrary/unrelated notes were handled appropriately; review-only files stayed identical. Earlier pre-correction 4/10-test runs are retained as history. Current source/records and package fingerprints are in `evals/loop-2026-10-26/`. |
| E7 | README, project map, publication instructions, security policy and design document distinguish public v0.6 from local v0.7 and implemented helpers from proposals. Package validation, skill-format validation and diff checks pass. GitHub readback confirms private reporting, vulnerability alerts and automatic security fixes enabled. |

Repository suite after review corrections: `python3 -B -m unittest discover -s tests -v` — 49 passed.
`scripts/validate.py`, `scripts/check_behavioral_evidence.py`, skill-creator format
validation, and Python dependency audit passed. Skills CLI 1.7.4 installed the local
package into a disposable project for all six targets; `.agents`, `.claude`, and
`.qwen` copies each matched all 27 source files; installed memory CLI starts.

CI now runs fixture replay and behavioral-record freshness checks alongside the
existing OS/Python matrix. Push runs are limited to main/tags to avoid duplicate
PR matrices. Action pins were updated from the existing green Dependabot proposals;
a separate media audit/type-check job and npm dependency updates were added. Hosted
execution of this changed workflow is still pending.

Marketing assets were preserved. Zod 4.6.7 overrides vulnerable transitive copies;
the refreshed lockfile audits clean, TypeScript passes, and SocialLoop frame 450
rendered. Remotion still warns about its old expected Zod pin. This bounded smoke
does not establish compatibility of every optional Remotion feature.

## Review and handoff

Durable final source and review receipts: [verification record](../evidence/evaluation-memory-checks/verification.md). Only that evidence-only directory is excluded from its final source manifest; this contract, implementation, tests, substantive lessons, and project records remain included.

All substantive source/docs are finalized before final capture. The final source
ID and independent review outcome are returned in separate review evidence and the
task handoff, not embedded back into this hashed record. Review is required before
claiming final readiness; a pending/failed review never becomes an automatic pass.

First fresh review found two introduced defects: R-CRLF-001 (clean CRLF checkout
falsely rejected by byte hashes) and R-CACHE-002 (normal memory CLI invocation wrote
an installed `.pyc`). Both were independently reproduced, given failing regression
tests, and corrected with LF attributes and bytecode suppression. Required current
behavioral evidence is refreshed after the helper correction; final return-review
status remains separate evidence so it cannot invalidate its own source packet.

Audit resolutions: destructive probes, optimized false passes, disabled security
reporting, stale project records, review finalization, lack of an evidence freshness
gate, media advisories, and duplicate CI have local fixes. Current learning evidence
is bounded to one run per scenario. Six-host installation does not prove six-host
model behavior. Controlled quality comparisons, other host runtime tests, new hosted
CI, and an immutable release/download test remain pending.

General inventory and arbitrary command-recording helpers remain optional proposals;
the new checker and fixed replay commands cover the demonstrated need without a
database, daemon, or new runtime dependency. No global installed skill was modified.
No commit, push, merge, or release was performed for this change.
