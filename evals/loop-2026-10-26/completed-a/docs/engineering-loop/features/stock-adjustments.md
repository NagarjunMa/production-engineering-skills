# Stock adjustments

Compact record as requested for the bounded README conformance fix. Significant
risk: shared library mutates a caller-owned dictionary. No external I/O.

## Contract and execution context

Source: `README.md`. Existing products accept positive, zero, and negative integer
deltas, including zero results; return and store the result. Unknown products raise
`KeyError`; negative results raise `ValueError`. Rejection preserves the entire
dictionary, and success preserves other products. Invalid types/dictionaries and
concurrency are excluded. All initial files and local callers were read before edits.

Verified locations: `inventory.py:adjust_stock` owns mutation (edit/review),
`tests/test_inventory.py:StockTests` is the sole local consumer and regression suite
(test/edit), and `README.md` owns the requirement (read). No Git baseline exists;
the supplied raw implementation is the pre-change baseline. New records live under
`docs/engineering-loop/`; no unrelated files are changed.

Design: keep the existing function and native dictionary `KeyError`; compute the
candidate quantity, reject negative values, then write once. No duplicate domain
rules, new helpers, dependencies, or I/O boundaries are needed. API, successful
results, and exception classes stay compatible. Correcting rejected mutations is
intentional. Local rollback is restoration of the five-line original function;
it reintroduces the defect. No release or production rollback is in scope.

## Acceptance and checks

| ID | Outcome | Test and plausible mistake rejected |
| --- | --- | --- |
| A1 | Return and store valid positive/zero/negative adjustments; zero is valid; preserve other products | `test_successful_adjustments`: a returned-only result, decrement rejection, zero rejection, or unrelated write fails |
| A2 | Negative result raises `ValueError` with entire dictionary unchanged | `test_negative_result_leaves_entire_stock_unchanged`: write-before-validate fails |
| A3 | Unknown product raises `KeyError`, preserves empty/nonempty dictionaries, for every delta sign | `test_unknown_product_leaves_entire_stock_unchanged`: inserting a default or checking negative delta first fails |

Behavioral red/green mode. Native command, from root:
`python3 -B -m unittest discover -s tests -v`.
Baseline: PASS, 1 existing test; it does not cover rejection. Added checks before
implementation: FAIL, 4 methods run and 2 negative-result subtests fail because
`A` becomes -1 instead of retaining 5 or 0. After the fix: PASS, all 4 methods
(six successful-adjustment, two negative-result, six unknown-product subcases).
Results apply to the final unchanged Python files; final source hashes go in
`../evidence/commands.md` and `../evidence/snapshot.json`.

## Handoff

Implemented locally; README contract passes local checks. Changed `inventory.py`
and `tests/test_inventory.py`; created this record, the project map, and evidence
records. No files removed. Self-review inspected all final Python code, all local
callers, errors, return/store behavior, and other-product preservation. Single rule
owner remains `adjust_stock`; no abstraction or duplicate production rule added.

Finding INV-1: confirmed pre-existing medium defect, original `inventory.py:2-4`:
mutation before negative-result rejection violates A2. The red test establishes
origin in the supplied raw source. Resolved locally by validation before mutation,
passing the regression and full native suite. No known remaining in-scope defect.

Scoped lesson: for this caller-owned dictionary operation, validate the candidate
quantity before assigning it. Exception-only assertions missed mutated state;
`test_negative_result_leaves_entire_stock_unchanged` now checks the entire mapping.

Next incomplete step: required fresh review, pending because task prohibits
delegation. Portable packet: `../evidence/review-packet.md`; zero reviewer rounds
used of a three-round default. Self-review cannot close this gate. Model identity
is unknown. No hosted checks, production readiness, deployment, or external consumer
testing is claimed. No configured lint/type/CI checks were found.
