# Verified project lessons

## Git inventory commands can execute configured hooks

- Scope: this package's read-only Git provenance helper; does not assert that every Git command executes hooks.
- Observed failure: independent v0.5 review configured a harmless `core.fsmonitor` sentinel and capture executed it four times through `git ls-files`, despite the no-source-execution contract.
- Correction: central Git wrapper sets `-c core.fsmonitor=false` for capture/check/validate commands. Keep Git invocation centralized so new subcommands inherit this restriction.
- Detection: `tests/test_review_evidence.py::ReviewEvidenceTests.test_repository_fsmonitor_is_not_executed` exercises all three commands. The sentinel regression failed before correction and passed afterward; independent return review confirmed it.
- Evidence: `evals/review-loop-2026-09-20/helper-review/review-round1.md`, `review-round2.md`, and their hash inventories. Future changes still require fresh verification.
- Boundary: disabling fsmonitor is not proof that arbitrary Git commands are safe. Inspect execution behavior before expanding the command set; preserve explicit no-network/no-repository-command scope.
