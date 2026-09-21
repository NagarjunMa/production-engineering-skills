# Learning-loop forward test: 2026-09-17

## Scope and setup

Skill: working-tree version 0.2.0, no committed revision. Runner: an independent Codex collaboration subagent with no inherited conversation history, using the same configured model as the parent. Exact host/model build identifiers were not independently captured. This is one local run, not a benchmark or cross-host compatibility test.

The disposable project initially contained only a README. The evaluator received the current skill path and this task: read the README, document the product/codebase, define feature evaluations, implement the stock-adjustment feature, and leave useful records for the next task. It could read the skill but write only in the isolated workspace. Network access, installations, commits, production systems, and external accounts were excluded.

The README specified Python standard-library code and unittest. Implement `adjust_stock(stock, sku, delta)` in `inventory.py` for a dictionary of nonnegative integer quantities: accept positive, zero, and negative integer adjustments to existing products; allow a result of zero; return and store the new quantity. Reject negative results with ValueError and unknown products with KeyError, leaving the entire dictionary unchanged on either error. Other input types, UI, databases, and packaging were out of scope.

## Observed artifacts and outcomes

The evaluator created exactly four files: `inventory.py`, `tests/test_inventory.py`, `docs/engineering-loop/PROJECT.md`, and `docs/engineering-loop/features/stock-adjustment.md`. The original README was unchanged.

The parent inspected all generated artifacts. The project map identifies the user goal, actual stack, file responsibilities, baseline, coverage, and remaining limits. The feature record maps seven criteria to independent expected results and named checks, distinguishes the initial README-only baseline from implemented files, and records executed results with source hashes. The evaluator reports recording the criteria before implementation; that chronology is reported by the evaluator rather than established by a separately retained execution trace.

`python3 -B -m unittest discover -s tests -v` passed with seven tests and 14 concrete cases, exit 0, on Python 3.11.1. The parent reran the suite successfully, then independently checked all combinations of starting quantities 0–7 and deltas -10–10 (168 cases), plus a missing-product case. Each valid result matched the requirement; rejected adjustments preserved the whole dictionary. This extra check validated the generated feature without using its implementation to produce expected answers.

The implementation reads the existing quantity, computes the candidate result, rejects underflow before mutation, then updates the selected entry and returns it. No unrelated features were added. No lesson file was fabricated because the run established no reusable failure or correction.

## Artifact fingerprints

SHA-256 identifiers reported by the evaluator for the tested source:

| Artifact | SHA-256 |
| --- | --- |
| README.md | `93f35bb949a5d334761d6068a5f23a8cf300ef091238fd762355bfa4d32a54af` |
| inventory.py | `9c0fe03a5767641860ca778aad68c915d6c58524180696d1a11e8015fd35be10` |
| tests/test_inventory.py | `3528ad8488b00f68f9d353ba67759a49515050fbad5e10c789568f47dcac359e` |

The disposable workspace is not a distributed fixture or installed skill resource. This record retains the test conditions and reviewed outcomes rather than private session transcripts.

## Limits

Passed for this bounded greenfield feature: project mapping, concrete evaluation artifacts, functional implementation, actual result recording, and restraint around unsupported lessons. No observed friction required changing the instructions. There was no runnable pre-change baseline, so the evaluator recorded that limitation rather than inventing a failing test.

Not tested: learning from an actual failed attempt, a second fresh session using saved context, stale-memory correction, exhaustive large-codebase inspection, probabilistic features, all read-only/narrow-scope scenarios, or activation in other coding hosts. No elapsed-time comparison or improvement over a no-skill baseline was measured. These remain scenarios to execute, not established benefits.
