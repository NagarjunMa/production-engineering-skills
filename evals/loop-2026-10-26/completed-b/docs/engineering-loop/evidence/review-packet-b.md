# Pending review: atomic batch stock adjustment

Source: `<evaluation>/session-b`; no Git/base exists. Integration target
is this supplied workspace only. Model identity unknown. No delegation was used
or authorized; reviewer rounds 0/3. Review is pending, not an independent verdict.

Read README, `../features/stock-adjustments.md`, `../PROJECT.md`, and `../LESSONS.md`.
Inspect `stock.py` and all of `tests/test_inventory.py`. Current locations replace
inherited `inventory.py` references. Requirements A1–A3 and B1–B5 cover native
single-item compatibility, ordered tentative quantities, repeated products,
intermediate underflow, rollback of late failures, first-error precedence, empty
batches, touched-only returns, and input preservation. Significant library risk.

Final current manifest: `snapshot-b.json`. Source/test/README/substantive records
are hashed; only evidence receipts are excluded. Earlier `snapshot.json`,
`context-before-rename.json`, `commands.md`, and `review-packet.md` are historical
session-a evidence and cannot establish current freshness. Session-b reported
checks and exact commands are in `commands-b.md`.

Portable prompt: review only, verify manifest freshness before/after, inspect
actual source against A1–A3/B1–B5, evaluate plausible wrong implementations from
the feature table, and independently run `python3 -B -m unittest discover -s tests
-v` from this workspace using read-only execution or an isolated matching copy.
Use standard-library/local tools only. No network, installs, commits, deployment,
source changes or delegation. Do not treat reported test results as independently
reproduced. Report actual identity/model (unknown if unavailable), context kind,
snapshot ID, inspected coverage, exact checks/results, limitations, verdict and
location-backed findings with stable IDs. Do not claim release approval.

Required review is pending under the supplied skill's “Obtain a fresh review when
warranted” rule: “For Significant/Critical work ... Delegate to a fresh reviewer
subagent when the host supports it and permissions permit.” The task expressly
prohibits delegation; self-review cannot satisfy the fresh-review requirement.
