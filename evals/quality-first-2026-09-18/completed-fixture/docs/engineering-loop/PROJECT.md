# Parcel project context

The [README](../../README.md) specifies a small Python quote library with web
and CLI consumers. Shipping policy is shared; output and error contracts differ
intentionally. There is no network, persistence, service, or deployment scope.

## Source map

- `parcel/policy.py`: `fee_cents` owns strict nonnegative integer validation and
  the 5000-cent free-shipping threshold.
- `parcel/web.py`: `web_quote` translates policy results/errors to web responses;
  `web_quotes` applies it to each input in order.
- `parcel/cli.py`: `cli_quote` formats CLI results/errors independently.
- `parcel/__init__.py`: empty package marker.
- `tests/test_quotes.py`: standard-library unittest checks for the entry points.

All six original files, including README, were read on 2026-09-18. No additional
repository instructions, dependencies, packaging, CI, or static-check configuration
were present in the project inventory. Python 3.11.1 is available; no supported
version range is declared. This disposable project has no Git metadata, so no
commit or clean-worktree claim is available.

## Feature and checks

[Batch web quotes](features/web-quotes.md) records the contract, current execution
context, design, and evaluation evidence. Single and batch quotes are implemented
and verified locally.

Run `python3 -B -m unittest discover -s tests -v` from the project root. Baseline:
3 tests passed on 2026-09-18 before changes. Final source: 9 tests passed on the
same date, covering ordered batches, invalid-item recovery, empty input, input
immutability, and existing web/CLI contracts. All final implementation and tests
were reviewed. No external consumer or release environment is available for inspection.
