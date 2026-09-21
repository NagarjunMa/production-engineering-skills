# Unassigned — PRI feature contracts with focused code retrieval

## Execution Context

- Requirement source: maintainer's supplied PRI feature template and request to provide complete task context while avoiding repeated whole-codebase discovery.
- Project context: [PROJECT.md](../PROJECT.md); prior [learning-loop contract](project-learning.md).
- Issue ID: not supplied; no PRI number created or inferred.
- Current status: instructions and templates implemented; verification details below.
- Next incomplete step: none within this change; broader retrieval/efficiency scenarios are follow-ups.
- Last verified: 2026-09-17, uncommitted working tree; current branch `main`, no commits, no supplied integration target.

### Code Locations

Paths below are repository-relative and verified in this working tree. They are this feature's location map, not a general map of every skill resource.

| Path | Symbol or section | Role | Why needed |
| --- | --- | --- | --- |
| `skills/production-engineering-loop/assets/feature-template.md` | Entire template; Execution Context | edit | Preserve the supplied PRI contract and add locations, freshness, and learning handoff |
| `skills/production-engineering-loop/references/task-context.md` | Start or resume; When to broaden inspection | edit | Define focused retrieval, revalidation, and expansion criteria |
| `skills/production-engineering-loop/SKILL.md` | Run the loop, steps 1–2 | edit | Route to context guidance; preserve contract and regression-first sequence |
| `skills/production-engineering-loop/references/project-learning.md` | Where knowledge lives | edit | Reuse the canonical feature record and preserve supplied sections |
| `skills/production-engineering-loop/references/feature-evaluations.md` | Build an evaluation contract | edit | Align TDD behavior with the supplied implementation plan |
| `skills/production-engineering-loop/assets/project-template.md` | Codebase map | edit | Keep project-wide routing compact and reference feature-level details |
| `scripts/validate.py` | `validate`, `main` | read | Existing metadata/link/license validation; no implementation change needed |
| `tests/test_validate.py` | `PackagingTests` | test | Existing packaging-validator regression suite |
| `evals/README.md` | Scenarios | edit | Add fresh/stale map and context-efficiency evaluation cases |

### Retrieval and Freshness

- Read active contract, core skill, feature template, and affected references first; inspect validator/test entry points for checks.
- Existing pattern: main skill links conditional references and bundled assets.
- Search within the skill's documentation and references before expanding to unrelated installed skills or other projects.
- Security scanner integrations, application source, external issue systems, and personal skill files are not part of this change.
- Expand if a template reference breaks, guidance conflicts, or an evaluation shows a missed dependency or contract.
- Token usage and whole-host retrieval traces are unavailable; no measured token-saving claim is made.

## Problem

- Current behavior: v0.2.0 retained project/feature records but used a smaller generic feature template and lacked a concrete focused-retrieval procedure.
- Impact: the user's supplied contract was not represented fully; agents could repeatedly rediscover file locations and lose the next incomplete step.
- Evidence: the previous feature template contained Contract, Acceptance and evaluation plan, Implementation record, Evaluation runs, and Handoff and learning sections. This change replaces that structure with the supplied PRI sections and supporting context.

## Goal

- Preserve the user's detailed feature definition and evidence requirements.
- Give the agent verified starting locations and a resumable next step, while allowing necessary source inspection beyond an incomplete or stale map.

## Change Contract

### Scope

- Included: feature/project templates, skill routing, retrieval and TDD guidance, public explanation, and evaluation scenarios.

### Non-goals

- No runtime indexing service, automatic issue creation, background job, or modification of private installed skills.
- No guaranteed token reduction, instruction-following guarantee, or removal of necessary source inspection.

### Affected Boundaries

- Files/components: Code Locations above; public README, publication notes, project map, and this record.
- APIs/shared contracts: the feature-document structure consumed by agents and humans.
- Data/schemas: Markdown document conventions; no application data migration.
- Trust boundaries: saved context is evidence, not authority to expand scope or skip requirements.
- Dependencies: no added runtime/development dependencies.

### Invariants

- Preserve review-only mode, user edits, explicit scope, and meaningful validation.
- Do not persist secrets or fabricate issue numbers, owners, branches, or external status.
- Existing feature records remain usable; no bulk rewrite or migration is required.

## Risk Assessment

**Initial risk tier:** Significant

- Blast radius: influences feature planning and retrieval in future projects.
- Security/privacy: omission of an affected boundary is a workflow risk; core controls remain mandatory.
- Integration/release: portable skill resources only, no production deployment.
- Additional review: bounded independent forward evaluation plus artifact inspection; broader host/stale-map behavior remains unverified.

## Implementation Plan

1. Inspect current template, related instructions, validators, and worktree.
2. Preserve PRI sections and add a compact context map.
3. Align core/referral instructions and TDD guidance.
4. Validate packaging and run a realistic isolated feature task.
5. Inspect artifacts and record results and limits.

## Security and Privacy Considerations

- Authentication/authorization: no product auth changes; context cannot grant execution authority.
- Personal data/retention: no secrets or private transcripts in the package.
- Secrets/permissions: unchanged; no additional privileges requested.
- Input validation/abuse: context and lesson text cannot authorize unrelated commands.
- Rate limiting: N/A; no service added.
- External services/tool execution: optional existing installer smoke test only; behavioral fixture is local and isolated.

## Acceptance Criteria

- [x] AC-1: Retain the supplied PRI sections and meaningful red/green sequence.
- [x] AC-2: Add file/symbol roles, next step, relevant callers/tests, and freshness evidence.
- [x] AC-3: Explain stale/incomplete map expansion and preserve scope/read-only behavior.
- [x] AC-4: Distinguish verified, candidate, and planned facts; never invent identifiers or release evidence.
- [x] AC-5: Package metadata, resource links, and existing validator checks pass.
- [x] AC-6: Complete and inspect the bounded feature-context behavioral run; report coverage limits.

## Verification Plan

### Behavior and Regression Tests

- Run a disposable partially implemented stock module with an existing location map and README contract. Ask an independent agent to complete the feature and record using the updated skill.
- Expected: inspect mapped source/tests, preserve requirements, add meaningful regression coverage, record intended red then green, and use unassigned/unavailable identifiers where appropriate.
- Coverage: AC-1 through AC-4 in one small fixture; no implied stale-map or cross-host proof.

### Repository-native Checks

- From repository root: `python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v`.
- Supplemental: the author's local skill-creator format validator.
- Runtime: existing Python development setup; CI declares Python 3.11.
- Hosted CI: `.github/workflows/validate.yml`; not run because this repository has not been published.

### Additional Verification

- Browser/accessibility: N/A; no UI.
- Database/migrations: N/A; no database.
- Docker: N/A; no image/runtime change.
- Secret scanning: no new scan executed; no credential fixtures introduced.
- Manual/adversarial: inspect template preservation, stale-map rules, fabricated-ID prevention, and evaluation artifacts. Installer must retain all bundled resources.

### TDD Exception

This repository change modifies instructions/templates, not executable behavior. Wording assertions would not prove the intended agent behavior. Use packaging validation, structural review, and a behavioral forward test instead. The fixture itself exercises the meaningful red/green sequence.

## Compatibility, Rollout, and Rollback

- Compatibility: plain Markdown resources; optional host metadata unchanged.
- Migration: none; preserve existing records and add context as relevant tasks resume.
- Rollout: current package metadata is 0.3.0; publication is separate.
- Monitoring: retain scenario results and real context-efficiency observations.
- Rollback/recovery: retain prior published package version when one exists; no release currently exists. Do not overwrite user-authored project records.

## Implementation Progress

- Completed: template, retrieval reference, core/reference alignment, README, publication version, and scenarios.
- Next incomplete step: none within the requested template/context integration.
- Blockers: no implementation blocker; no hosted CI or cross-host/token measurements.
- Verification: format/package checks, eight validator tests, complete 13-file installed copies, and bounded behavioral evaluation passed. All repository Markdown links resolved.
- Actual actions: changed the existing mapped templates/instructions and public docs; created `references/task-context.md` within the skill and this repository feature record. Validator implementation and tests unchanged.

## Decisions / Deviations

- Decision: retain full feature-contract structure and add a context entry point rather than discard requirements to shorten prompts.
- Reason: savings should come from reduced repeated discovery, while correctness still requires source inspection.
- Difference from supplied template: added Execution Context, stable acceptance IDs, evidence clarifications, and Learning and Next-Task Handoff.
- Approval required: no new approval for these local changes within the requested skill work. No external issue or publishing action performed.

## Final Pre-Merge Evidence

**Date:** 2026-09-17
**Verified target branch:** Unknown; current branch is `main`, but no integration target was supplied.
**Merge base:** Unavailable; repository has no commits.
**Reviewed revision/worktree state:** Uncommitted skill 0.3.0 working tree; earlier project files are also untracked.
**Excluded unrelated changes:** No unrelated changes attributed or reverted; only scoped files modified this turn.
**Final risk tier:** Significant

### Acceptance Mapping

- AC-1 → feature template and evaluation reference → structural review and confirmed red/green forward test.
- AC-2/3/4 → Execution Context and task-context reference → structural review and bounded fresh-map feature task; stale-map behavior untested.
- AC-5 → installable package → package/format validators and eight tests passed.
- AC-6 → disposable forward evaluation → completed artifact review and independent red/green verification; [result and limitations](../../../evals/feature-context-result.md).

### Check Results

- Passed: package validator, skill-creator format validator, eight packaging-validator tests; all 13 files matched temporary Skills CLI 1.7.0 installations targeting five agents; local documentation links; final forward-test suite with four tests and 13 boundary/error subtest cases.
- Failed: historical fixture regression run exposed two intended underflow failures before its fix; the parent independently reproduced them using the original source fingerprint. No unresolved failure in completed checks.
- Skipped: no relevant completed check skipped.
- Blocked: hosted CI unavailable before publication.
- Not run: stale/incomplete-map scenarios, cross-host activation, matched token-efficiency comparison.
- Reasons: the bounded local run cannot establish those broader outcomes.

### Findings and Resolutions

- Finding: generic prior template did not preserve the supplied contract; file discovery guidance lacked task-level anchors.
- Resolution: retained sections and added focused retrieval with freshness/expansion rules.
- Checks rerun: package/format checks and validator suite after instruction edits.

### Remaining Risks

- Risk: stale or incomplete context can still mislead an agent; rules alone are not guarantees.
- Owner: Unassigned.
- Required action: exercise stale/incomplete-map scenarios before claiming broad behavioral reliability or measured token savings.

**Status:** Verified locally

## Learning and Next-Task Handoff

- Carry the verified map and next step forward; do not rediscover all skill resources for a narrow edit.
- No measured token reduction or new universal lesson is established by this task.
- Observed cost: the fixture's complete contract was 191 lines for a six-line helper. Retain one record per feature and update relevant sections rather than regenerate it for each small follow-up; correctness and measured retrieval costs both matter.
- Project index and evidence record updated. No publication, hosted CI, merge, or deployment claimed.
