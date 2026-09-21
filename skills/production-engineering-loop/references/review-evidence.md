# Review evidence and optional helper

Use for fresh reviewer handoffs and supplied reports. The [packet template](../assets/review-packet-template.md) carries intent; the [helper](../scripts/review_evidence.py) records provenance. Neither proves correctness. Python 3.10+ and Git are needed only for the optional helper. The engineering workflow itself works during development, against uncommitted changes, or without Git/GitHub. Without the helper, record equivalent paths, hashes, timestamps, and source-state limitations manually.

## Capture

Resolve `SKILL_DIR` and `REPO` to the installed skill and target repository's absolute paths. Use an existing contract and a verified integration target; omit `--base` only if unknown/unborn, then report finding origin as unknown.

```sh
python3 "$SKILL_DIR/scripts/review_evidence.py" capture \
  --repo "$REPO" --base VERIFIED_TARGET_REF \
  --contract docs/features/my-feature.md \
  --output /absolute/scratch/review-before.json
python3 "$SKILL_DIR/scripts/review_evidence.py" check \
  --repo "$REPO" --packet /absolute/scratch/review-before.json
```

Output must be a new file outside source or in an explicit `--exclude` path. Capture refuses overwrites. Keep logs/reports outside source to avoid self-invalidating records. Exclusions are exact repository-relative paths/directory prefixes, not globs. Record why each is irrelevant; never exclude implementation, tests, requirements, or dependencies to obtain a pass. The contract cannot be excluded. Keep mutable progress records separate from requirements when practical.

The helper fingerprints all tracked/nonignored untracked files, including unchanged callers/configuration; it records the index separately and pins HEAD/base/merge base. It includes executable mode and symlink text. This is deliberately conservative. It captures twice and refuses a changing tree; pause writers anyway. It emits hashes/metadata, not source contents or environment values. Paths and hashes can still be sensitive; inspect artifacts before external sharing.

Every helper Git process is forced offline: lazy fetching and all Git transports are disabled, terminal prompting is disabled, optional locks are suppressed, and repository filesystem-monitor execution is disabled. A missing promised object therefore produces exit 2 and requires a locally available revision or manual evidence. Do not weaken these controls to make capture pass; the developer can choose a different locally available base or omit an unknown base and record origin as unknown.

Ignored inputs other than the explicit contract, installed dependencies, environment values, remote services, missing promised Git objects, and external symlink contents are outside this guarantee. Inspect relevant ones separately. Submodules, unmerged indexes, and unsupported filesystem types fail explicitly; use independent nested/manual evidence. A packet is not a signed attestation or source archive. The reviewer needs actual source; HEAD-only worktrees omit dirty changes.

Detected source/index/base changes make evidence stale. An agent can narrow which checks need rerunning, but must capture a new manifest and explain any retained historical evidence. Never replace IDs in old logs to imply reruns. Tests on an isolated copy must establish that copy matches the captured source. Exit codes: 0 current/structurally valid, 1 stale/inconsistent report, 2 input/capture error.

## Report schema version 1

Fill [review-report-template.json](../assets/review-report-template.json); remove the sample finding if none exist and replace placeholders. Equivalent Markdown is valid when machine validation is unavailable.

- `snapshot_id`: captured final ID; `schema_version`: 1.
- `reviewer`: actual identity, model and implementer_model strings or null, fresh_context boolean, kind self-review/fresh-context/cross-model/external. Cross-model requires distinct known models and a fresh context. Host evidence must substantiate the claim.
- `verdict`: no_material_findings/changes_required/blocked. The first requires listed required checks passing and no unresolved material findings. It is not release permission or proof that all checks were listed.
- `coverage`: source/acceptance mappings actually inspected; `limitations`: missing evidence/inspection.
- `checks`: unique id, exact command/manual procedure, result passed/failed/blocked/not_run/skipped, required boolean, snapshot_id, evidence/log reference with runtime/date. Structural checks are valid for non-executable findings.
- `findings`: unique id, severity critical/high/medium/low, material boolean, classification, origin, status, location, claim, criterion, evidence/confidence, reproducer, resolution, resolved_snapshot_id, check_ids.
- Classifications: confirmed/unsupported/ambiguous/pre-existing. Origins: introduced/pre-existing/unknown. Statuses: open/resolved/dismissed/deferred. Unsupported needs evidenced dismissal; ambiguous stays open; pre-existing needs verified baseline evidence.
- Resolved findings need a resolution, current snapshot, and referenced checks passing on that snapshot. Do not invent a test when structural verification is the appropriate evidence.

```sh
python3 "$SKILL_DIR/scripts/review_evidence.py" validate \
  --repo "$REPO" --packet /absolute/scratch/review-after.json \
  --report /absolute/scratch/review-report.json
```

Validation checks shape, consistency, and freshness, not truth/completeness of model identity, exclusions, baseline claims, outcomes, or review coverage. The coordinator inspects logs/source/host provenance and applies risk/human-review policy. Preserve earlier packets/reports as history.
