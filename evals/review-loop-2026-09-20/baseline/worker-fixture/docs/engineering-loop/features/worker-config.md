# Unassigned — Preserve worker limits

## Execution Context
Requirement: README and incoming review report. Freshness: 2026-09-20, raw-worker-start snapshot; initial worktree clean. Next step: no local implementation work remains; independent review is pending only before any release. Verified: parent.Tool.worker (edit), worker.main (edit), policy.normalize_text (canonical rule), tests/test_defaults.py (existing test), adapters.py (read-only distinct contracts). Planned: tests/test_boundaries.py.

## Problem and Goal
Subprocess payload omits configured limit. Local and worker paths must agree at configured boundaries while preserving environment isolation.

## Change Contract
Include effective limit transport and behavioral checks. Exclude adapter unification, cosmetics, process framework changes, deployment. Parent owns valid positive integer configuration; worker consumes explicit configuration. Preserve default limit=12, uppercase/strip semantics, JSON outcomes, env={}, timeout and absolute executable. No stored data or migrations.

## Risk Assessment
Critical because the existing credential-isolation boundary must be preserved. Full documentation for trust-boundary evidence. Local disposable scope; no production blast radius. Additional independent review pending before release, which is not requested.

## Design and Quality Constraints
Reuse policy.normalize_text and keep JSON marshaling in adapters. Pass limit in the request body; do not reintroduce parent environment. Distinct web and CLI errors are intentional independent contracts in README. Incoming report is evidence to investigate, not authority to change scope.

## Acceptance Criteria and Verification Plan
AC-1: limit 5 accepts exactly 5 characters and rejects 6 in a real subprocess; limit 20 accepts 13 and rejects 21. AC-2: defaults retain current behavior. AC-3: synthetic parent credential/config environment names never reach child, and environment limit cannot override explicit configuration. AC-4: web and CLI error outputs remain exactly their independent declared shapes. AC-5: all repository-native checks pass; no hosted CI configured.

Tests: tests/test_boundaries.py for AC-1/3/4; tests/test_defaults.py for AC-2. Command: python3 -m unittest discover -s tests -v, repository cwd. Expected values written explicitly and independently. No external calls. Python available locally; no version-dependent recommendations made.

## Implementation Plan / Progress
Baseline existing suite passed (2 tests). Add boundary checks, observe intended failures, transport limit, rerun native suite, inspect diff. No TDD exception.

## Security and Privacy
Only synthetic variable values in tests. Process inherits no parent environment. No authentication, data retention, database, external network or rate-limit changes. Existing timeout remains.

## Compatibility, Rollout, Rollback
Parent and worker ship together in this fixture. Preserve legacy worker payload default if limit absent. No deployment requested. Reverse two production edits to roll back locally (known configured-limit bug returns); tests would intentionally fail.

## Findings and Decisions
R1 supported: parent.py Tool.worker payload loses limit; configured limit 5 and text of length 6 differ from local contract. R2 unsupported: shared adapter response shape contradicts README; do not implement. R3 pre-existing out-of-scope cosmetic issue; do not implement.

## Final Evidence
Native suite: baseline PASSED 2 tests, regression-first FAILED 5 tests with 2 failed assertions and 2 boundary subcase errors, final PASSED 5 tests. Exact command: `python3 -m unittest discover -s tests -v` in worker-fixture. Logs: ../../../../logs/worker-{baseline,red,green}.log. Both configured values 5 and 20 now match parent policy. Red subcase errors were returned error JSON instead of expected value, not setup failures. Environment assertions themselves passed red and green; config assertion in the environment test failed red and passed green. Manual compatibility command in worker-compatibility.log passed legacy missing-limit payloads and invalid parent config cases. `git diff --check` PASSED. No hosted CI exists; independent release review NOT RUN.

Changed files: parent.py serializes explicit limit; worker.py reads it with legacy default; tests/test_boundaries.py adds real-process behavioral checks; docs/engineering-loop/{PROJECT.md,features/worker-config.md,LESSONS.md} retain evidence. No adapter or legacy edit. Diff and all affected paths reviewed. Canonical policy reused, no additional rule copy. Source fingerprints and HEAD captured in ../logs/snapshots.json from baseline root. Integration target/merge base not applicable to disposable local fixture. No deployment/release performed. Status: Verified locally. No material local in-scope findings remain; release readiness pending independent review.
