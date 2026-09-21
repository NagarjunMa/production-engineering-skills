# Feature-context forward test: 2026-09-17

## Setup

Tested the uncommitted v0.3.0 package with an independent Codex collaboration subagent using no inherited conversation history. Exact host/model build identifiers and token counts were not separately captured. The fixture was an isolated standard-library Python stock project containing five files: README, implementation, tests, project map, and a partial feature record with verified source locations. No issue identifier, Git metadata, hosted CI, or release target was supplied.

The task was to finish the documented stock behavior and complete the feature record using the updated template. The evaluator was allowed to read skill resources but write only within the disposable project; network, installations, commits, and external issues were excluded.

The README required positive, negative, and zero adjustments, valid zero resulting stock, KeyError for unknown codes, and ValueError on underflow with the whole dictionary unchanged. Unsupported types and concurrency were out of scope. The initial source performed mutation before the underflow check; the initial test covered only a successful increase.

## Results

- The evaluator read the five fixture files and the relevant skill entry point, project-learning, task-context, feature-evaluation guidance, and feature template. This is its reported access inventory, not an independently instrumented token trace.
- Baseline: `python3 -B -m unittest discover -s tests -v` passed one test.
- Regression-first: the expanded suite produced two intended underflow failures before the implementation fix.
- Fix: compute a candidate quantity and reject underflow before assigning it.
- Final: the same command passed four tests, including 13 boundary/error subtest cases, on Python 3.11.1.
- The parent inspected the implementation, tests, and final contract, and reran the final suite successfully. It reconstructed the fingerprint-matching original source in a separate temporary directory and confirmed the added tests produced the same two underflow failures.
- The feature record retained requirements and context, populated the supplied sections, refreshed actual locations and next-step status, and used an Unassigned title instead of inventing a PRI number. Git/CI/release evidence was correctly reported unavailable or not performed.
- The project map was updated; README remained unchanged. The local lesson was supported by a real defect and regression evidence and was explicitly limited to the in-memory behavior.

## Artifact fingerprints

Parent-verified SHA-256 values:

| Artifact | SHA-256 |
| --- | --- |
| README.md | `24d7db59e5c9d26f18464172f8ea08ee22a88dd02cdbb40a4622dea316f73d2f` |
| Original inventory.py | `c36e4cf518f95e8c1f6b553ef2f1a2759e3070c60602da2648c40059a2d83288` |
| Final inventory.py | `767502c2a31a139dd8d3e4f16254b38d358ded8f7e9ab688e80e085bc1ad958d` |
| Final tests/test_inventory.py | `ab8b91518ac992da5b1aeec8ef570603c35735767e262a22fbae53cd090760c8` |

## Cost and limits

The filled feature record was 191 lines for a six-line implementation. That is visible documentation overhead, not evidence of token savings. Keep one canonical feature record and update relevant sections on later tasks, using the compact entry point and source map to avoid rediscovery. The full supplied structure can remain valuable for requirements and review, but should not be regenerated for every small follow-up.

No matched baseline without the context map was run; no token counts or timing benefit were measured. All supplied code fit into one small module and test file, so this run cannot demonstrate avoidance of irrelevant code in a large repository. Stale/incomplete-map expansion, fresh-session reuse of this lesson, and other coding hosts remain untested. The run supports the observed regression-first workflow, record completion, and evidence handling only.
