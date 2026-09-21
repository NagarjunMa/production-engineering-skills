# Batch web quotes

## Contract and execution context

Source: [README](../../../README.md), inspected 2026-09-18. Implement
`web_quotes(subtotals)` with ordered, independently validated responses, empty
input support, and no input mutation. Preserve all existing fee, web, and CLI
contracts. Dependencies, services, persistence, and deployment are out of scope.

Standard risk: additive local orchestration within an established adapter, with
no policy change or new external boundary. Compact documentation fits this bounded
operation reusing existing domain policy and adapter behavior.

Verified paths: `parcel/web.py` (`web_quote`, `web_quotes`),
`parcel/policy.py` (`fee_cents`), `parcel/cli.py` (`cli_quote`), and
`tests/test_quotes.py` (entry-point consumers). Entire initial source snapshot
was inspected; there is no Git revision. Status: verified locally on 2026-09-18;
implementation and applicable checks are complete, with no next incomplete step.

## Design basis

Batch orchestration belongs in `parcel/web.py` and delegates each item to
`web_quote`. This keeps validation/pricing canonical in `fee_cents` and web
response translation canonical in `web_quote`. The CLI's distinct formatting
and error contract remain intentional. No broad exception handling, mutable
shared state, new abstraction, or dependency is needed. Adding a function is
compatible with existing entry points; local recovery is removal of that function.

## Acceptance and verification

| ID | Observable criterion | Independent evaluation in `tests/test_quotes.py` | Result |
| --- | --- | --- | --- |
| A1 | Responses preserve order and policy boundaries | `BatchQuotes.test_order_and_boundaries`: 5000, 0, 4999, 5001 with literal expected responses | Passed |
| A2 | Invalid items do not prevent later quotes | `BatchQuotes.test_invalid_items_do_not_stop_later_quotes`: negative, booleans, float, string, None, list, dict between valid values | Passed |
| A3 | Empty input returns an empty list | `BatchQuotes.test_empty` | Passed |
| A4 | Inputs remain unchanged | `BatchQuotes.test_input_is_not_mutated`: deep-copy comparison of mixed nested input | Passed |
| A5 | Existing entry points and policy remain compatible | `ExistingQuotes`: web/CLI threshold and invalid-type tests plus original tests | Passed |

Command: `python3 -B -m unittest discover -s tests -v`, project root,
Python 3.11.1. Baseline passed: 3 tests on the original source snapshot.
No configured lint/type/CI checks were found. External consumers are not available.

The same unittest command was run at three snapshots:

- Original source: **passed**, 3 tests, exit 0.
- Added tests with minimal `web_quotes` returning `[]`: **failed as intended**,
  9 tests with 9 assertion failures (8 invalid-item subtests and the ordering
  case), exit 1. Existing compatibility checks passed; this was a behavioral
  failure, not an import/collection error.
- Final implementation delegating to `web_quote`: **passed**, all 9 tests, exit 0.

`python3 --version` reported Python 3.11.1. `rg --files --hidden .` inventoried
the final eight files. `git status --short` reported that this is not a Git
repository; revision/diff metadata is unavailable. Final source was compared
against the initially read source and the applied patches. No network or hosted
checks were run, and no such checks are configured or required here.

## Outcome

Changed `parcel/web.py` by adding `web_quotes` and `tests/test_quotes.py` by adding
six behavioral tests while preserving the original three. Created
`docs/engineering-loop/PROJECT.md` and this feature record. No other project
files changed; no dependencies or infrastructure were added.

Design review traced batch to single-web adapter to shared policy, and inspected
CLI compatibility and all tests. There is no duplicated validation or price rule,
no batch-wide error catch that could discard later quotes, no input writes, and
no change to existing web/CLI functions. List construction provides ordered
responses and empty-input behavior. No material in-scope findings remain.

Project context is refreshed. No new reusable defect lesson was warranted: the
observed red state was the deliberate feature scaffold, not a discovered design
defect. Limits: one local Python version, no external consumers or Git history,
and no configured hosted/static checks. Non-iterable containers and exceptions
raised by a caller's iterator are outside the README contract; no new batch-level
error contract was introduced. Verified locally; nothing was released or committed.
