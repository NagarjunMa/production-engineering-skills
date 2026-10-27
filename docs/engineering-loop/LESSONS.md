# Verified project lessons

## Git inventory commands can execute configured hooks

- Scope: this package's read-only Git provenance helper; does not assert that every Git command executes hooks.
- Observed failure: independent v0.5 review configured a harmless `core.fsmonitor` sentinel and capture executed it four times through `git ls-files`, despite the no-source-execution contract.
- Correction: central Git wrapper sets `-c core.fsmonitor=false` for capture/check/validate commands. Keep Git invocation centralized so new subcommands inherit this restriction.
- Detection: `tests/test_review_evidence.py::ReviewEvidenceTests.test_repository_fsmonitor_is_not_executed` exercises all three commands. The sentinel regression failed before correction and passed afterward; independent return review confirmed it.
- Evidence: `evals/review-loop-2026-09-20/helper-review/review-round1.md`, `review-round2.md`, and their hash inventories. Future changes still require fresh verification.
- Boundary: disabling fsmonitor is not proof that arbitrary Git commands are safe. Inspect execution behavior before expanding the command set; preserve explicit no-network/no-repository-command scope.

## Acceptance assertions must not silently disappear

- Observed failure: `verify_outcomes.py` rejected the raw worker normally but printed PASS under optimized Python, because `assert` statements were removed.
- Correction and detection: assertion-based evaluators reject optimized execution. `tests/test_evaluation_tools.py::EvaluationSafetyTests.test_optimized_evaluators_fail_closed` covers all three runners.
- Applies when: a standalone acceptance evaluator uses assertions. This does not require replacing native unittest/pytest behavior or treating import errors as valid negative controls.

## Final receipts must not change the source they identify

- Observed failure: adding final results to a hashed feature document invalidated its review packet, even though implementation bytes were unchanged.
- Decision: finalize source and substantive records before capture; keep final snapshot IDs and later execution/review receipts in separate evidence. Requirements and substantive lessons remain included.
- Detection: `tests/test_review_evidence.py::ReviewEvidenceTests.test_final_documentation_precedes_capture_and_receipts_stay_separate` accepts evidence-only writes and rejects a changed contract.
- Applies when: source evidence includes project/feature documents. Excluding arbitrary documentation to force freshness is not a valid correction.

## Byte fingerprints need stable checkout representation

- Observed failure: fresh review R-CRLF-001 reproduced a clean Git checkout with `core.autocrlf=true` that changed byte hashes without a Git content change.
- Correction: repository attributes enforce LF for text and retain PNG/MP4/PDF binary bytes. The configured-checkout regression in `tests/test_behavioral_evidence.py` failed before attributes and passes afterward.
- Applies when: comparing retained raw-byte receipts across Git hosts. Do not normalize hashes after capture to hide actual source changes.

## Read-only helper tests must exercise normal invocation

- Observed failure: fresh review R-CACHE-002 confirmed that importing the adjacent helper wrote bytecode into the installed skill. Existing tests used `-B` and concealed that write.
- Correction: memory CLI disables bytecode writes before its local import. The plain-Python installed-copy regression in `tests/test_check_context.py` failed before correction and passes afterward.
- Applies when: a read-only CLI imports local modules. Verify the installed directory as well as the target project; caller flags are not a substitute for the tool's stated behavior.
