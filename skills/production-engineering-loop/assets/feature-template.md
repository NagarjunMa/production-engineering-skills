# PRI-<verified-number> — <Title>

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

- Intended behavior:
- Expected user or system outcome:

## Change Contract

### Scope

- Included:

### Non-goals

- Explicitly excluded:

### Affected Boundaries

- Files and components:
- APIs and shared contracts:
- Data and schemas:
- Trust boundaries:
- Dependencies:

Reference Code Locations for implementation paths rather than copying the table; describe boundary effects here.

### Invariants

- Behavior that must remain unchanged:
- Security and privacy guarantees:
- Backward-compatibility requirements:

## Risk Assessment

**Initial risk tier:** Trivial | Standard | Significant | Critical

**Rationale:**

- Blast radius:
- Security/privacy impact:
- Integration or release impact:
- Additional review required:

**Documentation mode:** Full — reason:

## Design and Quality Constraints

- Existing sound patterns and representative source locations:
- Canonical business rules or shared components to reuse:
- Module responsibilities, interfaces, state ownership, and dependency direction:
- Justified new pattern/boundary when absent; simpler alternative and tradeoff:
- Duplication to consolidate or intentionally retain, with semantic reason:
- Applicable repository requirements and standards, with version/source where needed:
- Evidence for these constraints: source/caller review, existing architecture checks, or behavior tests:

Keep this specific to the change. A small project may need only cohesive functions; do not invent layers, standards obligations, or abstractions to fill the section.

## Implementation Plan

1. Inspect existing implementation, history, tests, and dirty worktree.
2. Identify completed work and the next incomplete step.
3. Select behavioral change, pure refactor, or non-executable validation mode; add relevant checks.
4. For behavioral changes confirm the intended failure; for pure refactors establish passing characterization coverage; for non-executable work record structural validation.
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

- [ ] AC-1: <Observable behavior>
- [ ] AC-2: <Negative or failure-path behavior>
- [ ] AC-3: <Compatibility requirement>
- [ ] AC-4: <Security/privacy requirement>
- [ ] AC-5: Relevant repository-native checks pass.
- [ ] AC-6: No unresolved material findings remain.

Adapt criterion IDs to the feature and keep them stable. Explain inapplicable example criteria; do not check a box to imply unperformed verification.

## Verification Plan

### Behavior and Regression Tests

- Validation mode: behavioral change | pure refactor | non-executable; rationale:
- Plausible wrong implementation for each material criterion and detecting check:
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

- Review policy, actual reviewer identity/model/context, rounds used/budget:
- Reviewed packet/snapshot ID and freshness result:
- Finding:
- Stable ID, classification, origin, materiality, and supporting/contrary evidence:
- Resolution:
- Reproducer, final source snapshot, and verification evidence:
- Checks rerun:
- Design review evidence: pattern fit, canonical rule reuse, modularity, dependency boundaries, and affected consumers:

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
