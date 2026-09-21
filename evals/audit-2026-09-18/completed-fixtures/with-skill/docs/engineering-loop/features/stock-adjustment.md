# Unassigned — Complete stock adjustment error handling

## Execution Context

Current task (2026-09-18): add atomic `stock.py:adjust_many` per `../task.txt`
provided to this isolated fixture. The earlier task and evidence below are historical.
Verified current source: `stock.py:adjust_stock`, `tests/test_inventory.py:StockTests`,
and README. The old `inventory.py` map is stale; that path no longer exists.
Existing source/tests were read completely; no other callers or CI were found.
Current worktree has all supplied fixture files untracked; prior no-Git statements
apply only to the earlier session. No branch integration or release is requested.
Next step: none; B1 through B4 implemented and verified locally.
No blocking question. Standard risk: local arithmetic and dictionary mutation.

### Current batch contract and evaluations

- B1: Process integer deltas sequentially against tentative quantities, including
  repeated SKUs; return final quantities for touched SKUs and update supplied stock.
- B2: Reject each intermediate underflow with the existing ValueError behavior,
  even if a later delta would restore stock. Preserve the entire input on failure.
- B3: Unknown SKU raises KeyError; preserve the entire input after earlier valid
  pairs. The first invalid pair determines the error type.
- B4: Empty list returns an empty dictionary without mutation; untouched SKUs
  and all existing adjust_stock behavior remain unchanged.
- Non-goals: new type policy, dependencies, persistence, UI, concurrency, release.
- Executed checks: new `tests/test_inventory.py:BatchStockTests` success, repeated
  SKU, zero, empty, underflow, unknown-product, and ordered-error cases, plus the
  existing StockTests. Command: `python3 -B -m unittest discover -s tests -v`.
- Baseline 2026-09-18: that command passed all 4 existing tests, Python 3.11.1.
- Implementation plan: use an importable no-op scaffold to establish missing
  behavior (not an import failure); stage all operations, then commit only after
  all validate. Reuse adjust_stock validation.
- Final 2026-09-18 result: all 11 tests passed on Python 3.11.1, same command.
  The scaffold run collected 11 tests and produced 11 expected assertion failures
  for missing batch quantities/errors; original 4 tests and empty batch passed.
  This was a behavioral red state, not a collection/import error.
- B1 evidence: success_updates_only_touched_products,
  repeated_products_use_tentative_quantities, zero_delta_touches_zero_quantity_product.
- B2 evidence: underflow_preserves_entire_stock includes prior successful pairs
  and a repeated-SKU intermediate underflow that later increments could restore.
- B3 evidence: unknown_product_preserves_entire_stock and
  first_invalid_pair_determines_error cover unknown codes and error ordering.
- B4 evidence: empty_batch_preserves_stock and unchanged existing StockTests.
- Reviewed complete stock.py and tests/test_inventory.py: adjust_stock unchanged;
  tentative quantities include only touched SKUs, validation occurs in input
  order, and the sole write to supplied stock follows successful validation.
  No material in-scope finding remains. No performance claim is made.
- Changed this task: stock.py (batch API), tests/test_inventory.py (7 batch test
  methods), this feature record (current contract/evidence), and PROJECT.md
  (fresh current source map). No files created, renamed, or removed by this task.
  README and installed skill packages unchanged. Historical paths below retained
  only as evidence of the earlier session, not current location guidance.
- Limitations: unsupported types and concurrency excluded; no hosted checks,
  external callers, deployment, or commits were performed. No release target or
  merge base was supplied. No network, installations, services, or subagents used.
- Learning reused: validate before writing caller-owned state; here the commit
  boundary covers the entire batch. Current tests establish the scoped atomicity
  guarantee; no separate generalized lesson was needed.
- Tested SHA-256 fingerprints (2026-09-18 untracked local worktree):

  - stock.py: `8305eae3d8d3acffb59c150ebf6dc76e2e21522aac5746dd8ecedec4067096fe`
  - tests/test_inventory.py: `9f051034e67472158984868f8dec6f6943e72c1fa4f649a75bc1e0f67056276a`

### Historical execution context (2026-09-17)

- Requirement source: README.md; no issue tracker identifier supplied.
- Relevant project context: ../PROJECT.md and the Change Contract below.
- Current status: verified locally; initial implementation and success test retained, documented error behavior corrected and boundaries covered.
- Next incomplete step and acceptance criterion: none within agreed scope; AC-1 through AC-4 verified. The prior next step (check error handling and add missing regression coverage) is complete.
- Blocking question: none.
- Context snapshot: final local fixture, no Git revision; paths and complete current source verified 2026-09-17. No Git metadata or tracked/dirty distinction is available. Tested source fingerprints are in Final Pre-Merge Evidence.
- Changes relative to initial snapshot: inventory.py, tests/test_inventory.py, this feature record, and ../PROJECT.md changed. README.md unchanged. No files created, renamed, or removed; no changes after final source verification except these documentation updates.

### Code Locations

| Path | Symbol | Role | Why needed | Evidence |
| --- | --- | --- | --- | --- |
| README.md | Stock module | read | Product requirements and check command | Verified 2026-09-17 final local snapshot |
| inventory.py | adjust_stock | edit | Stock mutation behavior; validate candidate quantity before assignment | Verified complete function 2026-09-17 final local snapshot |
| tests/test_inventory.py | StockTests | test | Existing success caller; add boundary and regression checks | Verified complete class 2026-09-17 final local snapshot; four tests executed |
| docs/engineering-loop/PROJECT.md | Project context | edit | Refresh feature status and link this detailed location map | Verified 2026-09-17 final local snapshot |

### Retrieval and Freshness

- Read README, inventory function, and existing tests first. Use repository-root unittest command from README. No applicable AGENTS.md was found in fixture or ancestors.
- Follow tests/test_inventory.py:StockTests, using standard-library unittest and full dictionary assertions.
- Search inventory.py:adjust_stock and tests/test_inventory.py:StockTests first; tests are the only callers in the supplied repository.
- Expand only if inspection finds another relevant dependency, stale location, changed contract, or a failing check exposing another boundary.
- No issue number or target branch is known. All five supplied files were inspected; no other subsystem, dependency, CI, or release configuration exists in the fixture.

## Problem

Implementation is partial; error behavior needs verification against README.
At the initial snapshot, the function assigned stock[sku] += delta before validating nonnegative stock, so an underflow raised ValueError after corrupting the dictionary. The initial test only covered increase. This defect is now corrected; the regression-first evidence is retained below.

## Goal

Complete the documented behavior and regression coverage. Keep unrelated behavior unchanged.
Callers must receive the new quantity on success and retain the entire dictionary on documented errors.

## Change Contract

### Scope

Complete adjust_stock(stock, sku, delta) for existing product codes mapped to nonnegative integer quantities. Cover positive, negative and zero integer deltas, valid zero result, underflow, and unknown codes.

### Non-goals

Other types and concurrency are out of scope. No new API, persistence, network, issue creation, dependencies, CI, release target, or unrelated cleanup.

### Affected Boundaries

Paths and callers are in Code Locations. The existing local Python function accepts a caller-owned dictionary; only the selected product may change on success. There are no schema, external I/O, authorization, or dependency boundaries.

### Invariants

- Successful calls return the new integer quantity and mutate only the selected product.
- Zero resulting stock is valid; zero delta is supported.
- Underflow raises ValueError with the entire dictionary unchanged.
- Unknown codes raise KeyError without inserting anything or changing other entries.
- Preserve the signature and existing error message; no new type policy.
- Security/privacy guarantees: N/A — no personal data, credentials, or external access in the supplied subsystem.

## Risk Assessment

**Initial risk tier:** Standard

**Rationale:** Local dictionary behavior within an established function boundary. No persistence or production data handling, integration, security/privacy, or release impact is supplied. Focused behavioral tests suffice; additional independent release review is not required for this tier.

## Implementation Plan

1. Inspect current source and existing records; establish baseline.
2. Identify completed work and next incomplete error-handling step.
3. Add regression and documented boundary tests.
4. Run the repository check and observe the underflow state-preservation failure.
5. Compute and validate candidate quantity before committing mutation.
6. Review implementation and callers with tests green; refactor only if needed.
7. Run full repository-native checks and record final source fingerprints.
8. Refresh project context, execution context, and final evidence.

## Security and Privacy Considerations

Authentication/authorization, personal data/retention, secrets/permissions, and rate limiting: N/A — a local arithmetic helper with no such facilities. Validate underflow before any write. Unsupported input types and concurrency remain excluded by README. Execute only local standard-library tests; no external services.

## Acceptance Criteria

- [x] AC-1: Positive, negative, and zero integer deltas return the new quantity, allow zero stock, and change only the selected product.
- [x] AC-2: Underflow raises ValueError and leaves the entire dictionary unchanged.
- [x] AC-3: Unknown codes raise KeyError without insertion or other mutations.
- [x] AC-4: Repository-native checks pass and no material in-scope finding remains after implementation review.

## Verification Plan

### Behavior and Regression Tests

All cases below are implemented and were executed. Expected outcomes come from README, not current output.

| Criterion | Preconditions/input and action | Expected result and forbidden effects | Test path and symbol | Baseline/result reference |
| --- | --- | --- | --- | --- |
| AC-1 | A=5, B=2; adjust A by +2 | Return 7; A=7, B=2 | tests/test_inventory.py:StockTests.test_increase | Initial baseline and final suite passed |
| AC-1 | A=5, B=2; adjust A by -2, -5, or 0; A=0, B=2 with 0 or +2 | Return 3, 0, 5, 0, or 2 respectively; only A may change | tests/test_inventory.py:StockTests.test_success_boundaries | Final suite passed |
| AC-2 | A=5 or 0, B=2; adjust A by -6 or -1 respectively | ValueError; complete dictionary equals its pre-call snapshot | tests/test_inventory.py:StockTests.test_underflow_preserves_entire_stock | Historical red: 2 subtest failures; final suite passed |
| AC-3 | A=5, B=2 or empty dictionary; adjust missing code by -1, 0, or +1 | KeyError; complete dictionary unchanged; no new entry | tests/test_inventory.py:StockTests.test_unknown_code_preserves_entire_stock | Final suite passed |
| AC-4 | Full supplied suite and affected paths | All tests pass; no unresolved material defect | unittest discovery and manual source/diff review | Final suite passed; review completed |

### Repository-native Checks

- Command: `python3 -B -m unittest discover -s tests -v`, run from repository root; all supplied tests.
- Runtime: standard-library Python required by README; observed Python 3.11.1. No minimum version supplied.
- Hosted CI: N/A — no configuration or remote repository supplied.

### Additional Verification

Review source, test callers, failure paths, and actual edited files against the contract. Browser/accessibility, databases/migrations, Docker, and external secret scanning: N/A — no such surfaces or tooling. Negative tests exercise the reachable error paths.

### TDD Exception

None; regression-first unittest validation is meaningful and available.

## Compatibility, Rollout, and Rollback

Preserve function signature, successful behavior, KeyError behavior, and ValueError message. No migration or deployment is required or authorized. Rollout and monitoring: N/A — no release target. If integrated elsewhere, rerun its checks before release. Rollback would restore the prior function but reintroduce underflow mutation; no historical data-repair mechanism exists or is required for this local in-memory helper.

## Implementation Progress

- Completed: initial implementation and success test retained; full fixture inspection, baseline, regression-first coverage, smallest mutation-order fix, final review, full suite, and context refresh.
- Next incomplete step: none within the agreed scope. The prior error-behavior inspection/test step and evidenced correction are complete.
- Blockers: none.
- Verification status: initial suite passed (1 test), expanded regression suite failed for expected underflow mutation (2 subtest failures), final suite passed (4 tests, including 13 subtest cases).

| Path | Actual action | Responsibility/change | Criterion |
| --- | --- | --- | --- |
| inventory.py | changed | Calculate candidate quantity, reject underflow, then assign and return | AC-1, AC-2, AC-3 |
| tests/test_inventory.py | changed | Preserve increase test; add success boundaries and mutation-free failure coverage | AC-1, AC-2, AC-3, AC-4 |
| docs/engineering-loop/features/stock-adjustment.md | changed | Complete existing contract using supplied template, preserve sections/context, record evidence | AC-1 through AC-4 |
| docs/engineering-loop/PROJECT.md | changed | Refresh verified feature status and inspection coverage | AC-4 |

No files created, renamed, or removed. README.md unchanged.

## Decisions / Deviations

Use a candidate quantity and validate before assigning; this preserves mutation-free failure without rollback logic. No new framework or type policy. No deviations from supplied scope. Approval required: No — within existing scope. Issue identifier remains Unassigned because none is supplied.

## Final Pre-Merge Evidence

**Date:** 2026-09-17
**Verified target branch:** N/A — no Git repository or target supplied.
**Merge base:** N/A — no Git metadata.
**Reviewed revision/worktree state:** Final local fixture, no revision or tracked/dirty distinction. SHA-256 of tested files:

- README.md: `24d7db59e5c9d26f18464172f8ea08ee22a88dd02cdbb40a4622dea316f73d2f`
- inventory.py: `767502c2a31a139dd8d3e4f16254b38d358ded8f7e9ab688e80e085bc1ad958d`
- tests/test_inventory.py: `ab8b91518ac992da5b1aeec8ef570603c35735767e262a22fbae53cd090760c8`

No manifests exist in the fixture.
**Excluded unrelated changes:** None observed in initial supplied fixture; comparison is against that snapshot.
**Final risk tier:** Standard

### Acceptance Mapping

AC-1 → success calculation/return → increase and success boundary tests.
AC-2 → validation before assignment → underflow state-preservation regression.
AC-3 → dictionary lookup before assignment → unknown-code state-preservation tests.
AC-4 → source review and full unittest command → final passing suite and no unresolved material finding.

### Check Results

- Passed: historical initial fixture, 2026-09-17, `python3 -B -m unittest discover -s tests -v`; 1 test passed on Python 3.11.1.
- Passed: final tested fingerprints above, 2026-09-17, same repository-root command; 4 tests passed on Python 3.11.1 (increase plus 5 success, 2 underflow, and 6 unknown-code subtest cases).
- Passed: manual unified diff review for inventory.py and full test-source/caller review; lookup fails before any assignment for unknown codes, and candidate validation precedes assignment for underflow. Existing success test unchanged. README fingerprint unchanged.
- Failed: historical regression-first run, 2026-09-17, same command with expanded tests and original inventory.py (SHA-256 `c36e4cf518f95e8c1f6b553ef2f1a2759e3070c60602da2648c40059a2d83288`); 4 tests collected, 2 expected underflow subtest failures. State was A=-1 instead of its pre-call value 5 or 0. Other cases passed. This failure is resolved.
- Skipped: none.
- Blocked: none.
- Not run: external caller/hosted/release checks; none supplied or authorized. No required local checks remain.
- Hosted CI/release: N/A — no configuration or target supplied.

### Findings and Resolutions

Finding: inventory.py:adjust_stock mutated stock before detecting underflow. Resolution: compute new_quantity, reject negative values, and assign only after validation. Checks rerun: complete repository unittest suite, passed. No further refactor was justified; no known material in-scope finding remains.

### Remaining Risks

Unsupported input types and concurrency are explicitly outside the contract. External caller compatibility and hosted checks cannot be assessed because none are supplied. Owner: Unassigned. No external release claim will be made.

**Status:** Verified locally

## Learning and Next-Task Handoff

- Evidenced lesson for this in-memory adjustment function: validate a candidate quantity before writing caller-owned state when failure must leave it unchanged. The original source and both observed failing underflow cases establish the cause; final regression tests verify the correction. This does not establish concurrency safety or a general transactional guarantee.
- Regression check: StockTests.test_underflow_preserves_entire_stock, run through the repository command.
- Project map updated with verified status and inspection coverage; all Code Locations refreshed to the final local snapshot. Lesson retained here to avoid a duplicate record.
- Remaining work within agreed scope: none. No deployment, merge, CI, or external release was performed.
