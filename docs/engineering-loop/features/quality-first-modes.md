# Unassigned — Quality-first engineering and documentation modes

## Execution Context

- Requirement source: maintainer clarification on 2026-09-18. Code quality across multiple AI-assisted projects is the primary objective; token efficiency is secondary. Compact and full documentation modes are essential.
- Mode: Full — shared skill behavior and contract/template routing change across tasks.
- Source state: local uncommitted repository; no release revision or integration target is established.
- Current status: implemented and locally verified with package checks, preservation checks, and bounded compact/full scenarios.
- Next incomplete step: none within this refinement; publication and broader evaluation remain separate work.

| Path | Responsibility | Location state |
| --- | --- | --- |
| `skills/production-engineering-loop/SKILL.md` | Quality objective, reference routing, mode selection, completion conditions | Verified; changed |
| `skills/production-engineering-loop/references/code-quality-review.md` | Existing/missing design baseline, canonical rules, applicable quality bar | Verified; changed |
| `skills/production-engineering-loop/references/documentation-modes.md` | Compact/full rules and escalation | Created |
| `skills/production-engineering-loop/assets/feature-compact-template.md` | Compact contract, design, evidence, handoff | Created |
| `skills/production-engineering-loop/assets/feature-template.md` | Full user PRI structure with design evidence | Verified; changed |
| `skills/production-engineering-loop/references/{feature-evaluations,project-learning,task-context}.md` | Consistent references to both modes | Verified; changed |
| `skills/production-engineering-loop/agents/openai.yaml` | Quality-focused invocation metadata | Verified; changed |
| `README.md`, `evals/README.md`, `docs/engineering-loop/PROJECT.md` | Intent, usage, evaluation scenarios, current context | Verified; changed |

## Problem

- The prior audit emphasized token efficiency beyond the maintainer's intended priority.
- The skill already covered quality, but routed its detailed quality reference primarily to substantial cleanup/architecture work.
- Short-task guidance and the full feature-template requirement left documentation depth ambiguous.

## Goal

Require a justified, repository-grounded design and meaningful behavioral evidence during ordinary implementation. Support early-stage and small projects without imposing production-scale infrastructure. Make documentation depth explicit without reducing the applicable quality bar.

## Change Contract

### Scope

Quality-first positioning, routine design review, guidance for missing architecture, and compact/full documentation selection with consistent template routing.

### Non-goals

Plugin manifests, publication, runtime memory/index automation, new tool dependencies, broad agent benchmarks, and a promise of defect-free code. The historical audit remains a record of its reviewed snapshot.

### Affected Boundaries

Shared skill instructions, bundled references/templates, host UI metadata, and public usage guidance. No application API, production data, schema, or external service changes.

### Invariants

Preserve the user's full PRI sections and requirements, review-only behavior, scope/permission boundaries, current-source verification, independent acceptance expectations, and honest blocked/not-run reporting. No automatic deployment or rewriting project experience into the installed skill.

## Risk Assessment

**Initial risk tier:** Significant — shared instructions affect implementation decisions across projects. No production mutation. Independent bounded forward testing complements package checks; no claim of universal host behavior.

## Design and Quality Constraints

- Reuse the existing skill/reference/template architecture rather than introduce a runtime.
- Keep detailed design review canonical in code-quality-review.md and mode selection canonical in documentation-modes.md; entrypoint routes to them.
- Both templates retain behavioral and design evidence. The full template preserves all prior headings in their existing order.
- Apply sound repository conventions with source evidence; do not copy known defects, force named patterns, or merge semantically distinct rules.
- Existing instructions and packaging format govern this edit; no new standard or certification obligation is introduced.

## Implementation Plan

1. Inspect current skill, quality/reference routing, supplied template, evaluations, and worktree.
2. Clarify the primary objective and design baseline for existing/new projects.
3. Add compact/full rules and the compact template; preserve and extend full PRI content.
4. Update callers, public guidance, UI metadata, and project context.
5. Run package checks and a bounded independent behavioral evaluation; inspect actual artifacts.
6. Record results and remaining coverage limits.

## Security and Privacy Considerations

No secret/customer-data collection or new permissions. Existing trust-boundary, critical-review, and authorization rules remain. Evaluation uses a disposable local library with no network, installation, or production access.

## Acceptance Criteria

- AC-1: Quality is explicitly primary; speed/context efficiency never justify omitting relevant investigation or checks.
- AC-2: Substantive implementation routes through evidence-backed architecture, modularity, redundancy, and design-pattern review, including missing/inconsistent architecture.
- AC-3: Compact/full selection is unambiguous, preserves supplied contracts, and does not waive risk or checks.
- AC-4: Both formats retain relevant design and behavioral evidence; existing PRI headings remain.
- AC-5: Package checks pass and a bounded independent run demonstrates compact-mode behavior with canonical-rule reuse and preserved consumer contracts.

## Verification Plan

### Behavior and Regression Tests

An independent agent receives a small Python library with a canonical fee policy and distinct web/CLI adapters, then implements the documented batch quote feature. Review actual source for policy reuse and absence of speculative layers, and verify behavior independently. Keep evaluator expectations out of its prompt.

### Repository-native Checks

- `python3 -B scripts/validate.py`
- `python3 -B -m unittest discover -s tests -v`
- Supplementary local skill-creator quick-validator.
- Compare full-template heading sequence with its retained pre-change source; inspect mode/reference links and required fields.

### Additional Verification

Inspect full-mode, greenfield, escalation, and review-only instructions for conflicts. These inspections are not execution evidence for those scenarios. No hosted checks or native host discovery are claimed.

### TDD Exception

The package changes are instructions and document templates, not executable application behavior. Use structural validation, preservation checks, and an independent agent run rather than tests that merely assert prose strings. The disposable feature implementation should follow the skill's applicable behavioral testing sequence.

## Compatibility, Rollout, and Rollback

Existing standalone skill structure and host paths remain. Added references/templates require copying the whole v0.4.0 package. No data migration or rollout is performed. To roll back locally, restore the prior package snapshot as a unit; published version/release management remains pending.

## Implementation Progress

- Completed: instruction, template, reference, README, evaluation-scenario, metadata, publication-version, implementation-design overview, and context edits; independent evaluation and final artifact review.
- Next incomplete step: none for the requested refinement.
- Blockers: none known for local package/evaluation work.
- Verification status: passed locally within the stated scope; broader scenarios and native hosts untested.

## Decisions / Deviations

- Preserve all supplied full-template sections; add a separate compact option instead of replacing the contract.
- Treat zero harmful rule duplication as the aim; intentional contract differences may remain.
- Keep the audit historical. This clarification changes priority, not the previously measured results.
- Approval required: No — within the maintainer's requested skill refinement. Publication and external changes are outside this work.

## Final Pre-Merge Evidence

**Date:** 2026-09-18
**Verified target branch / merge base:** unavailable; no integration target or initial commit.
**Reviewed worktree:** uncommitted local source; version metadata 0.4.0.
**Excluded changes:** prior audit artifacts and historical evaluations are retained, not rewritten.
**Final risk tier:** Significant.

### Acceptance Mapping

- AC-1 → SKILL.md opening, README, project intent → source inspection confirms quality-first objective and secondary efficiency.
- AC-2 → ordinary quality-reference routing and design-baseline guidance → compact run reused canonical policy/adapter and preserved intentional CLI differences; parent source review confirmed no copied rule or speculative layer.
- AC-3 → documentation-modes.md and consistent callers → compact implementation chose a short record; full planning retained the supplied contract and changed only the authorized plan.
- AC-4 → both templates and design/evaluation reference → all 29 prior full-template headings retained in order; observed records retain material design and behavioral evidence.
- AC-5 → package and independent checks → results below and [retained evaluation evidence](../../../evals/quality-first-2026-09-18/README.md).

### Check Results

- Passed: package validator; all eight validator regression tests; supplementary skill-creator quick-validator.
- Passed: one-time structural comparison preserved all 29 previous full-template headings in order; changed document links resolve.
- Passed: compact fixture's final nine-test suite independently rerun; 1,111 bounded batch cases and 20 existing-entrypoint cases passed the separate checker. A deliberately invalid filtering implementation failed that checker.
- Passed: parent review of full plan confirmed all 29 supplied headings and five checked requirement lines retained, with all eight other files byte-identical. Acceptance remained unchecked and the API unimplemented as requested.
- Agent-reported: compact baseline three tests and intended scaffold assertion failures; full planning's fresh nine-test baseline. Parent independently checked final behavior/artifacts, not the intermediate scaffold.
- Not run: hosted CI, native host discovery, broad architecture/greenfield/risk-escalation scenarios, and comparative quality benchmark. No failed or blocked local required check remains.
- Snapshot limitation: uncommitted source. Evaluation records retain artifacts and tested skill hashes; explicit-invocation test copy has identical behavior instructions but the previous UI prompt metadata. Final UI metadata passed package checks; native UI invocation was not tested.

### Findings and Resolutions

The ambiguous small-record/full-template routing is replaced by one mode-selection reference. Callers in the entrypoint, learning, evaluation, and retrieval references were inspected for consistency. Public version guidance was updated to 0.4.0. No material in-scope finding remains in the inspected changes; broader behavior is not inferred from these examples.

### Remaining Risks

Instruction following varies by model/host. One small fixture cannot establish general code-quality improvements. Further behavioral scenarios remain unexecuted unless specifically recorded.

**Status:** Verified locally within the bounded evidence above; not published or universally validated.

## Learning and Next-Task Handoff

The maintainer's product priority is code quality across projects; retain that explicit decision in PROJECT.md. Do not infer a token-efficiency optimization task from the existence of a context map.
