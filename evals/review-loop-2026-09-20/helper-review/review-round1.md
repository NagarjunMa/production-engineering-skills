# Independent v0.5 review — round 1

Reviewer: /root/v05_review, fresh delegated context. Model identity unavailable; no cross-model claim. Read-only source review with copied package/tests and mutating probes restricted to this scratch directory. Contract read: docs/engineering-loop/features/automated-review-resolution.md. Verdict: changes_required.

## F1 — High: disable repository-configured fsmonitor execution

- Location: skills/production-engineering-loop/scripts/review_evidence.py:22–24 (Git wrapper), triggered by ls-files at lines 76 and 88.
- Classification: confirmed, material, open. Origin: introduced in v0.5 (helper absent from supplied v0.4 package).
- Claim: shell=False does not prevent Git from executing a configured core.fsmonitor command. Capture, check, and validate all reach these Git calls and therefore can execute arbitrary repository-configured commands with agent permissions during an operation advertised as no-source-execution.
- Contract: deterministic helpers must avoid arbitrary command execution; repository content does not grant authority; helper docstring promises no source execution.
- Reproducer: run `python3 probes.py` here. The fixture creates a local Git repository, configures core.fsmonitor to an isolated harmless shell hook that appends a sentinel, then calls capture. Observed: capture exit 0; fsmonitor-ran contains `invokedinvokedinvokedinvoked`.
- Correction: override core.fsmonitor=false on helper Git calls, audit other implicit Git executable/network mechanisms relevant to these commands, and add a focused regression proving capture/check/validate never invoke the configured hook.
- Existing unit tests all pass despite this defect.

## Coverage and checks

Inspected entire helper, unit tests, SKILL.md, independent-review.md, review-evidence.md, execution-boundaries.md, codex-review.md, reviewer prompt, packet/report templates, and reviewer TOML. Read code-quality-review.md as review guidance. Assessed path confinement, symlink privacy, untracked/index/deleted freshness, report status/check constraints, read-only/fallback/model-identity instructions, recursion limits and finite resolution policy. No other material defect established.

- `python3 -m unittest discover -s tests -v`: PASS, 22 tests, isolated copied source.
- `python3 scripts/validate.py`: PASS after adding the root LICENSE omitted from the initial scratch copy. Initial failure was fixture setup, not package defect.
- `python3 probes.py`: FAILS the intended no-execution invariant as above; probe process completes successfully and records observed failure.
- Reviewed-file hashes match source at review completion. Full copied package hash inventory: reviewed-hashes.json.

Limitations: no release commit/base exists in the main repository; hashes identify reviewed source. Did not execute live model fallback or install/load the TOML in a host; instruction assessment is structural. Did not assess parent-owned README/eval revisions. Runtime environment and ignored/external dependencies remain outside helper guarantee as documented. Static review does not establish exhaustiveness.
