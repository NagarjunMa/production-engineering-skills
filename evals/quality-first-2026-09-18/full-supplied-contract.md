# Unassigned — Currency-aware quote API

Use a PRI number only when verified from the supplied issue or repository issue source; record that source. Otherwise use `Unassigned — <Title>`. Do not invent identifiers or create external issues. Preserve supplied sections. Use `N/A — reason` for inapplicable fields and `Unknown — next verification step` for missing evidence. Distinguish planned work from completed work and historical results from current evidence.

## Execution Context

Compact entry point for this task; it does not replace the requirements below. Reuse existing project documents rather than maintaining duplicate plans.

- Issue/requirement source:
- Relevant project context and decisions (paths/anchors):
- Current implementation status:
- Next incomplete step and acceptance criterion:
- Blocking question, if any:
- Context last verified: date, source revision/snapshot, dirty worktree state:
- Changes since that verification, including uncommitted/untracked files:

### Code Locations

| Repository-relative path | Symbol, section, or route | Role: edit/read/test/config | Why needed and intended change | Evidence: verified/candidate/planned; source snapshot |
| --- | --- | --- | --- | --- |

Include affected callers, shared contracts, representative existing patterns, and test entry points. Planned files are not existing verified locations. Re-resolve symbols before editing; line numbers are hints. Keep the map bounded to this feature.

### Retrieval and Freshness

- Read first, in order (including relevant scoped repository instructions):
- Existing pattern to follow, with path and symbol:
- Search these modules first; exact symbol/path queries if useful:
- Areas not needed initially and why (revisit if evidence connects them):
- Expand inspection when: a symbol is missing/renamed, callers/contracts differ, dependencies/configuration change, a check exposes another boundary, or context is stale:
- Remaining inspection gaps or unresolved locations:

## Problem

- Current behavior:
- Problem and impact:
- Supporting repository evidence:

## Goal

- Intended behavior: Plan a new public `web_quote_currency(subtotal, currency)` API. Support only USD. Unsupported currency returns status 400 and error "unsupported currency"; for USD retain existing subtotal validation and fee policy, and include currency "USD" on successful responses.
- Expected user or system outcome:

## Change Contract

### Scope

- Included:

### Non-goals

- Explicitly excluded: Currency conversion, external services, implementation during this planning task, dependency changes, and deployment.

### Affected Boundaries

- Files and components:
- APIs and shared contracts:
- Data and schemas:
- Trust boundaries:
- Dependencies:

Reference Code Locations for implementation paths rather than copying the table; describe boundary effects here.

### Invariants

- Behavior that must remain unchanged: Existing web_quote, web_quotes, and CLI output/error shapes remain byte-for-byte compatible in serialized content; the new API is additive.
- Security and privacy guarantees:
- Backward-compatibility requirements:

## Risk Assessment

**Initial risk tier:** Trivial | Standard | Significant | Critical

**Rationale:**

- Blast radius:
- Security/privacy impact:
- Integration or release impact:
- Additional review required:

## Implementation Plan

1. Inspect existing implementation, history, tests, and dirty worktree.
2. Identify completed work and the next incomplete step.
3. Add or update regression tests.
4. Run tests and confirm failure for the intended reason.
5. Implement the smallest coherent change.
6. Refactor with tests green.
7. Run incremental repository-native checks.
8. Prepare final verification evidence.

Keep changes reviewable and exclude unrelated work. Focus inspection using the location map. Record a justified TDD exception below when executable testing is not meaningful; unavailable tools/services are blockers. Missing imports, empty test collection, or setup failures do not by themselves establish the intended behavioral regression.

## Security and Privacy Considerations

- Authentication and authorization:
- Personal data and retention:
- Secrets and permissions:
- Input validation and abuse prevention:
- Rate limiting:
- External services and tool execution:

## Acceptance Criteria

- [ ] AC-1: New API returns currency USD on successful USD quotes and preserves the canonical fee policy.
- [ ] AC-2: <Negative or failure-path behavior>
- [ ] AC-3: Existing web_quote, web_quotes, and CLI contracts stay unchanged.
- [ ] AC-4: <Security/privacy requirement>
- [ ] AC-5: Relevant repository-native checks pass.
- [ ] AC-6: No unresolved material findings remain.

Adapt criterion IDs to the feature and keep them stable. Explain inapplicable example criteria; do not check a box to imply unperformed verification.

## Verification Plan

### Behavior and Regression Tests

- Test:
- Expected result:
- Acceptance criterion covered:

For multiple cases, use one compact mapping:

| Criterion | Preconditions/input and action | Expected result and forbidden effects | Test path and symbol or manual procedure | Baseline/result reference |
| --- | --- | --- | --- | --- |

### Repository-native Checks

- Exact commands, working directory, and selection scope:
- Supported runtime and source:
- Required hosted CI checks and source:

### Additional Verification

- Browser/accessibility:
- Database/migrations:
- Docker:
- Secret scanning:
- Manual or adversarial checks:

### TDD Exception

If executable testing is not meaningful, explain why and identify structural or repository-native validation instead. Record evidence and limitations. If testing is meaningful but unavailable, record a blocker and its missing prerequisite.

## Compatibility, Rollout, and Rollback

- Compatibility constraints:
- Migration requirements:
- Rollout sequence:
- Monitoring:
- Rollback procedure:
- Recovery/data-integrity considerations:

## Implementation Progress

- Completed:
- Next incomplete step:
- Blockers:
- Verification status:

Keep the Execution Context's next step consistent with this section. Record actual file changes, excluding unrelated user edits:

| Path | Actual action: created/changed/renamed/removed | Responsibility/change | Criterion |
| --- | --- | --- | --- |

## Decisions / Deviations

- Decision:
- Reason:
- Difference from approved plan:
- Approval required:

Reuse existing authorization. Record `No — within existing scope` where applicable; seek a decision only at an unresolved boundary. Do not rewrite a valid acceptance criterion to obtain a passing test.

## Final Pre-Merge Evidence

**Date:**
**Verified target branch:**
**Merge base:**
**Reviewed revision/worktree state:**
**Excluded unrelated changes:**
**Final risk tier:**

Verify the intended integration target and merge base; do not assume `main`. If Git, a target branch, or commits are unavailable, record that limitation. Include dirty-state information and evaluated file/manifest fingerprints when a commit alone does not identify the tested code.

### Acceptance Mapping

- Criterion → implementation → evidence:

### Check Results

- Passed:
- Failed:
- Skipped:
- Blocked:
- Not run:
- Reasons:

For each executed check retain command/procedure, date, tested source snapshot, result, and limitations. Skipped/not-run checks are not passes. Keep older runs labeled as historical.

### Findings and Resolutions

- Finding:
- Resolution:
- Checks rerun:

### Remaining Risks

- Risk:
- Owner:
- Required action:

Use `Unassigned` rather than inventing an owner.

**Status:** Planned | Implemented locally | Verified locally | Ready for PR | Merged | Deployed

Select only an evidenced state. Report blocked verification separately. Hosted checks must be passed or explicitly pending; local execution does not prove hosted CI results. Merged/Deployed require observed external evidence and relevant authorization.

## Learning and Next-Task Handoff

- Evidenced failure/correction and scoped lesson, if one emerged:
- Regression check or detection procedure:
- Project-map or lesson-record updates:
- Context locations refreshed or invalidated:
- Remaining work within the agreed scope:

Reference existing lessons instead of duplicating them. A completed task need not invent a lesson or future work. In review-only mode, propose record updates without writing them.
