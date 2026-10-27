# Fresh release review — 2026-10-26

Verdict: **changes_required**. Two confirmed material findings. This is a review result, not release authorization.

Reviewer: Codex fresh reviewer subagent; exact model/build unknown. Fresh-context review of the supplied contract and source; no implementation conversation was supplied. Independence kind: fresh-context, not cross-model or human review. Risk: Significant. Applied repository Ponytail full guidance and the bundled production-engineering-loop reviewer/code-quality instructions.

Base/HEAD: `4501e91d555222ec53873bd13c3671fb59714c5e`.
Packet: `<scratch>/pel-final-review-20261026.json`.
Snapshot: `24ec010956560032bd6f0d95a80a8dfc3a4b5af3a6b47a38f490cd8b8b3276a9`.
Contract: `docs/engineering-loop/features/evaluation-memory-checks.md`.
Packet freshness passed before inspection and after all checks. Source was not edited.

## R-CRLF-001 — Enforce checkout line endings before comparing retained byte hashes

- Severity: **medium**; material: **yes**; confidence: high.
- Classification: confirmed; origin: introduced; status: open.
- Narrow location: `scripts/check_behavioral_evidence.py:25-26`; consumer: `.github/workflows/validate.yml:29,44`; underlying byte hashing at `scripts/check_behavioral_evidence.py:14-17`.
- Affected contract: E4b freshness guard and E7 portable validation/CI. Byte-exact evidence is appropriate, but its source checkout representation must be deterministic.
- Reachable failure: a fresh checkout with `core.autocrlf=true` converts tracked text to CRLF. The repository has no `.gitattributes` and the workflow sets no checkout line-ending policy. The guard rejects the skill and retained artifacts as changed and asks for fresh model evaluations even though `git diff --exit-code` reports no content change. This breaks the new required guard in supported CRLF-configured Git checkouts, relevant to the Windows matrix. The actual hosted runner's effective Git configuration was not queried, so this report does not assert an observed hosted failure.
- Independent reproduction: copied every regular packet file into a disposable repository, initialized an index without creating a commit, removed the copied working files, and ran `git -c core.autocrlf=true checkout-index --all`. `SKILL.md` then contained CRLF, `git -c core.autocrlf=true diff --exit-code` returned 0, and `python -B scripts/check_behavioral_evidence.py` returned 1 with `Skill changed or evidence is incomplete` plus artifact-change errors.
- Reproducer: `python3 -B <scratch>/pel-crlf-reproducer-20261026.py <repository>`. Full results: `<scratch>/pel-crlf-results-20261026.json`.
- Smallest correction: enforce LF for the byte-hashed text source/evidence during checkout, preferably through repository attributes, preserving exact byte-integrity checks. In a second disposable case, adding `* text=auto eol=lf` before indexing produced LF, a clean Git diff, and guard exit 0 under the same `core.autocrlf=true` configuration. No source correction was applied. Add a configured fresh-checkout regression and rerun affected validation after correction.

## R-CACHE-002 — Suppress imported-helper bytecode writes in the read-only CLI

- Severity: **medium**; material: **yes**; confidence: high.
- Classification: confirmed; origin: introduced; status: open. Originally raised by the coordinator and independently reproduced by this reviewer.
- Narrow location: `skills/production-engineering-loop/scripts/check_context.py:12`; masking test invocation: `tests/test_check_context.py:29` always supplies `-B`.
- Affected contract: E3's read-only memory tool and E7's read-only/no-silent-installed-update documentation. `references/context-checks.md` shows normal Python invocation without `-B` and calls the checker read-only.
- Reachable failure: using the documented command normally imports the adjacent `review_evidence.py` and creates `scripts/__pycache__/review_evidence.cpython-311.pyc` inside the installed skill. This changes installed files merely to inspect memory. The project records remain unchanged, but the broader read-only claim is false. Current subprocess tests pass `-B`, so they suppress the behavior rather than test the normal CLI.
- Independent reproduction: copied only both helper files into a clean disposable `installed/scripts/`, created a temporary non-Git project with PROJECT.md and app.py, removed inherited Python bytecode-suppression/cache-prefix environment variables, and invoked `python check_context.py capture --repo <project> --record PROJECT.md --source app.py` without `-B`. Exit 0; before/after comparison found the new cache directory and `.pyc`. No source/installed host file was changed by this review. Evidence: `<scratch>/pel-cache-results-20261026.json`.
- Smallest correction: disable local bytecode writes before importing the adjacent helper, and add a clean installed-copy subprocess test using the documented plain Python command. Compare the whole installed helper directory and target project before/after. Recheck capture and check paths without relying on the caller's `-B` or environment.

## Source and acceptance coverage

Inspected actual implementations and CLI boundaries, not only diffs: both new repository scripts; installed `check_context.py`; adjacent provenance/path/fingerprint helper; all affected/new tests; historical probe entry points and all three assertion-based evaluators; current single-item evaluator, prompts, retained A/B implementations/tests, stale receipt, scoped lessons, read-only fixture and observation; package validator; workflow/dependabot configuration; changed skill instructions, templates and relevant references; current contract/project memory and public/publishing/security/media documentation. Inspected the media dependency declaration/lockfile change for the Zod override, but did not re-audit or render media. Historical broken `starting` and `review-only` code was treated as evaluator input.

| Criterion | Evidence and plausible wrong implementation assessed |
| --- | --- |
| E1 | Shared temporary-directory probe and both wrappers inspected. Fresh sentinel tests execute both scripts and ensure caller-owned files survive; old caller-root writes would fail them. |
| E2 | All three historical evaluators guard `__debug__` before evaluating; fresh tests use real fixture arguments under `-O`. Replay checks also cover optimization refusal. The new single evaluator uses explicit raises rather than assertions. Removing guards would expose optimized false success. |
| E3 | Eight black-box tests pass for non-Git, changed/deleted/renamed record/source, malformed/tampered receipt, escape/symlink inputs and read-only operation. Existing project receipt passes. Current B pre-rename receipt independently returns stale with PROJECT.md, inventory.py and test import changes. A checker that silently refreshed or ignored selected missing files would fail. **R-CACHE-002 remains open**: normal invocation writes an installed helper cache, which the `-B` tests hide. |
| E4 | Runner's fixed argument-array commands, temporary copies, fingerprints, negative markers, timeouts and exclusive external receipt writes inspected. All 14 controls pass; test rejects a missing import masquerading as expected failure. A runner scoring every nonzero result as success would fail that test. |
| E4b | Current guard passes; mutation/incomplete-record tests pass. The guard intentionally checks consistency, not execution truth. **R-CRLF-001 remains open**: a logically unchanged fresh checkout can be falsely rejected. |
| E5 | Finalization guidance/templates and provenance integration test inspected; test accepts separate evidence writes and rejects changed requirements. Packet remains current after review. A helper excluding the contract or treating changed requirements as current would fail. |
| E6 | Retained outputs/source and notes inspected. Fresh scratch A/B native suites pass 4/10 tests. Restoring original A implementation produces exactly 2 failures; substituting B `return {}` scaffold produces exactly 7 failures. Replay independently passes 336 A and 7,422 B cases. Read-only zero-limit defect independently reproduced in memory. A mutation-before-validation implementation or empty batch scaffold is detected. Fresh-context execution chronology and original complete before/after comparisons remain reported history; no new model runs were performed. |
| E7 | Local package/link validator, tests, diff check and current/substantive documentation inspected. Public v0.6/local v0.7, byte checks versus semantics, replay versus live behavior, same-host bounded evidence and pending hosted/runtime checks are distinguished. Remote security settings and GitHub readback are reported history, not freshly verified here. |

## Checks actually run

Runtime: Python 3.11.1, local macOS environment, 2026-10-26. Commands below ran against the packet source; test writes used disposable directories and receipts went to `/tmp`.

- Passed: `python3 -B skills/production-engineering-loop/scripts/review_evidence.py check --repo . --packet <scratch>/pel-final-review-20261026.json` at start and finish.
- Passed: `python3 -B -m unittest discover -s tests -v` — 47 tests, 24.370 seconds.
- Passed: `python3 -B scripts/run_evaluations.py --output <scratch>/pel-review-replay-20261026.json` — 14 fixture/control checks, source unchanged.
- Passed: `python3 -B scripts/validate.py`.
- Passed: `python3 -B scripts/check_behavioral_evidence.py` on the original LF worktree.
- Passed: `python3 -B skills/production-engineering-loop/scripts/check_context.py check --repo . --receipt docs/engineering-loop/project-context.json`.
- Passed: `git diff --check`.
- Passed: scratch A/B native suites and intended red reconstructions; `<scratch>/pel-release-review-checks-20261026.json` records commands' outputs and outcomes. The same harness independently checked the stale continuation receipt and reproduced the intentional read-only zero-limit defect.
- Confirmed failure: documented memory CLI invocation without `-B` creates installed helper bytecode in a clean scratch copy; `<scratch>/pel-cache-results-20261026.json`.
- Confirmed failure and demonstrated correction: configured fresh CRLF checkout, then same procedure with scratch LF attributes; reproducer/results cited in R-CRLF-001. Git content stayed clean in both cases; guard changed from exit 1 to exit 0.

The parent-supplied 47-test/14-check results were treated as history until independently rerun above.

## Limits

No network/external service checks, hosted CI, actual Windows execution, fresh agent behavior trials, installer/network dependency audits, full media render, exhaustive repository audit, or cross-model review were performed. Remote security controls, action revision validity, existing release/install provenance and live-agent isolation remain supplied historical claims. Exact retained artifact consistency and current deterministic behavior do not authenticate original execution or prove general quality improvement.

Skipped unrelated cleanup and additional dependency tooling. Remaining material risks are the open CRLF checkout failure and imported-helper bytecode writes; hosted CI and remote release/security assertions require their own evidence.
