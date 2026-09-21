# v0.5 review-loop evaluation

Local execution date: 2026-09-20. Host: Codex desktop; bundled CLI reports `0.154.0-alpha.6.2`; Python 3.11.1. Actual delegated model identities were not exposed, so reports use `fresh-context`, never `cross-model`. All work used synthetic local fixtures, no credentials or external services.

## What was exercised

- v0.4 baseline: configured worker bounds, synthetic credential isolation, mixed review suggestions, canonical-rule refactor, distinct web/CLI errors, and a dynamically resolved public helper.
- v0.5: the same raw starting fixtures, updated skill, automatic fresh reviewer delegation inside the task, structured reports, finding dispositions, source fingerprints, and post-review stale-source rejection.
- Deterministic helper tests: real committed/dirty/unborn Git repositories, staging-only drift, rename/deletion/new files/dependencies, contract changes, exclusions, symlinks, integrity, malformed reports, unsupported cross-model claims, unresolved findings, and required-gate failures.
- Independent package review: a real Git fsmonitor execution defect was found, reproduced, fixed centrally, and verified on capture/check/validate. See `helper-review/review-round1.md` and `review-round2.md` with reviewed hashes.

## Outcomes and limits

The v0.4 baseline already solved both tasks: worker 5 tests passed after meaningful red/green; refactor 6 characterization tests passed before and after. v0.5 worker: 9 tests passed plus fresh reviewer-selected comparisons, with R1 resolved and unsupported R2/R3 rejected. No quality-improvement percentage is supported. The mixed report supplied the worker defect, and the baseline agent constructed the fixtures, so this is an unblinded workflow evaluation, not a blind defect-discovery benchmark.

The v0.5 refactor passed four characterization tests before/after and 37 assertions selected by its fresh reviewer. The checks protect distinct adapter errors and a deployment-registry consumer. Semantic ownership still requires source inspection: output checks alone cannot prove that duplication was removed appropriately. Both candidate reports passed the evidence CLI's current-snapshot/structure validation, and the coordinator reran independent fixture acceptance checks.

The staleness negative control deliberately disabled freshness in a disposable helper copy. The committed/dirty test failed because changed source was incorrectly accepted. `staleness-negative-control.log` retains that intended failure. The initial helper test run before the file existed was a scaffold/setup failure and is **not** counted as behavioral red evidence.

The independent acceptance runner initially assumed unchanged lowercase worker output. Inspection established the fixture's pre-existing strip/uppercase contract, so that expectation was corrected before scoring. The corrected runner fails the raw worker on lost configured limits and passes the completed worker; this test correction is not presented as an implementation fix.

A baseline report write encountered a transient disk-space failure; already-written code/logs were preserved and later copied. Subsequent local checks completed. No release, remote CI, broad host compatibility, model diversity, TOML loading, or retry-budget exhaustion claim follows from these runs.

The no-delegation forward test produced a portable packet/prompt, reran nine tests in a byte-matched isolated copy, verified the incoming findings, and kept the explicitly required fresh cross-model review pending. Source hashes stayed unchanged. This simulates an unavailable host capability; it does not exercise a second vendor's product.

## Retained artifacts and reproduction

- `baseline/raw-worker-start/` and `baseline/raw-refactor-start/`: shared starting inputs.
- `baseline/worker-fixture/`, `baseline/refactor-fixture/`: v0.4 outputs; `baseline/logs/`: historical runs/diffs/hashes.
- `baseline-skill-sha256.json`: v0.4 source identity.
- `candidate/`, `candidate-refactor/` and matching `*-evidence/` / `*-review-evidence/` directories: final v0.5 source, tests, packets and reports. Each report names original scratch locations and snapshot; logs are retained by basename in the corresponding evidence directory.
- `helper-review/`: independent findings and correction evidence; probe scripts retain original scratch locations as historical reproduction context. Portable regression is in `tests/test_review_evidence.py`.
- `fallback-evidence/`: portable handoff and read-only review with required cross-model evidence explicitly pending.
- `verification/`: final main-source manifest and repository-native check logs; this output directory is excluded from its own manifest only. The fresh package review is tied to the package/test hash inventory; final documentation and evidence integration were reviewed by the coordinator.

From repository root:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
python3 evals/review-loop-2026-09-20/verify_outcomes.py worker evals/review-loop-2026-09-20/baseline/raw-worker-start
```

The last command **must fail** on configured-bound rejection. Run it against `baseline/worker-fixture` or the retained candidate for a pass. Run `verify_outcomes.py refactor <fixture>` for dynamic-consumer/adapter assertions. It executes synthetic fixture code; do not run it against untrusted external source.

Raw Git metadata is omitted from copied fixture directories. Recorded historical commit IDs are fixture provenance, not commits in this uncommitted skill repository. To create fresh provenance, initialize a disposable copy of a raw fixture, commit the starting files, overlay completed source, and capture with the evidence helper. Do not substitute new IDs into historical reports.
