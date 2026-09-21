# Automated independent review and findings resolution

## Execution Context

### Target Repository and Source Snapshot

- Repository root: this `production-engineering-loop` repository.
- Planning state: uncommitted working tree; no release commit exists yet.
- Target package: `skills/production-engineering-loop/`.
- Evidence inspected: current skill instructions, reference documents, templates, behavioral evaluations, and the PRI-19 reviewer report supplied by the maintainer.

### Relevant Paths

- `skills/production-engineering-loop/SKILL.md`
- `skills/production-engineering-loop/references/feature-evaluations.md`
- `skills/production-engineering-loop/references/code-quality-review.md`
- `skills/production-engineering-loop/references/documentation-modes.md`
- `skills/production-engineering-loop/references/project-learning.md`
- `skills/production-engineering-loop/assets/`
- `evals/README.md`
- `docs/self-learning-implementation.md`

### Relevant Commands and Constraints

- Existing validation: `python3 scripts/validate.py`
- Existing tests: `python3 -m unittest discover -s tests -v`
- The core skill must remain useful in coding agents without Codex subagents, hooks, or a CI integration.
- A reviewer must evaluate an identified source snapshot. Reviewing an unspecified or subsequently changed worktree is insufficient evidence.
- A second model is stronger evidence than self-review, but model disagreement is not proof. Executable behavior and repository evidence remain authoritative.

## Problem

### Behavior Before v0.5

The skill directs the implementing agent to self-review and supports an external review report through ordinary conversation, but it does not define a complete reviewer handoff or a machine-checkable findings lifecycle. The maintainer currently opens a second task, supplies the problem statement, identifies the branch, asks another model to review it, and manually returns the report to the implementation task.

The PRI-19 exercise exposed the practical gap. The implementation and its existing tests looked sound, but an independent boundary probe showed that configured parser limits disappeared when execution crossed into a worker. The same report then had to be copied back manually before the implementation agent could verify and resolve it.

### Problem and Impact

- Independent review is optional in practice because the workflow is manual and repetitive.
- The reviewer may receive an incomplete contract, wrong base revision, stale worktree, or insufficient verification history.
- Findings are free-form. There is no required classification as confirmed, unsupported, ambiguous, or pre-existing.
- A code edit can be reported as a resolution without reproducing the defect and rerunning the affected checks.
- Existing acceptance tests may prove the intended implementation while failing to reject a plausible wrong implementation.
- Self-review and different-model review are not distinguished in the final evidence.

### Supporting Repository Evidence

- `SKILL.md` includes self-review and critical-work review guidance but no reusable independent-review protocol.
- `feature-evaluations.md` maps criteria to checks but does not require a negative control for high-risk criteria.
- `docs/self-learning-implementation.md` proposes helpers but does not implement snapshot or review-report validation.
- `evals/README.md` does not contain a lost-configuration execution-boundary scenario or a true/false reviewer-findings resolution scenario.

## Goal

### Intended Behavior

Add a finite review-and-resolution stage that can run automatically inside a capable host and degrade to a portable review packet elsewhere. The implementing agent should:

1. Capture the requirements, base, reviewed source snapshot, changed paths, relevant project context, and verification evidence.
2. Ask a fresh reviewer context to inspect the code when the host supports delegation.
3. Label the actual independence level used.
4. Verify every material finding against current source and the change contract.
5. Classify the finding as `confirmed`, `unsupported`, `ambiguous`, or `pre-existing`.
6. Fix confirmed in-scope findings, add a reproducer or regression check when meaningful, and rerun affected checks.
7. Re-review the resulting snapshot until no material confirmed finding remains or a concrete blocker is recorded.
8. Promote only verified, reusable lessons into project memory, with their evidence and scope.

### Expected Outcome

The user should not need to create a second chat or repeatedly paste the same problem statement. A review result should remain useful because it names exactly what was reviewed and records how each finding was resolved. The core package should still work in other AI coding tools through explicit prompts, templates, and deterministic local helpers.

## Change Contract

### Scope

#### Included

- Evaluate implementation options for the six previously identified improvements.
- Define portable contracts for review packets, review reports, finding classifications, freshness, and stopping conditions.
- Define optional Codex-native delegation that launches a fresh reviewer in the same task.
- Define deterministic helpers that capture and compare Git/worktree snapshots without deciding whether code is correct.
- Add behavioral evaluations that can falsify the new instructions.
- Preserve compact and full documentation modes.

### Non-goals

- Training or updating model weights.
- Treating a model review as an approval authority.
- Requiring every host to support subagents or model selection.
- Automatically merging, deploying, or accepting security-critical work.
- Executing arbitrary repository commands merely because they appear in a review packet.
- Claiming universal model independence when reviewer and implementer share a provider, prompt family, or tools.

### Affected Boundaries

- Skill instructions and references: review policy and findings-resolution workflow.
- Assets: portable review packet/report templates and optional configuration examples.
- Local scripts: snapshot capture, report validation, and freshness comparison.
- Behavioral evaluations: boundary, mutation, staleness, and reviewer-disagreement scenarios.
- Optional host adapters: Codex subagent/custom-agent configuration and later CI/plugin packaging.

### Invariants

- Repository evidence outranks reviewer assertions.
- A reviewer cannot silently expand implementation scope or user permissions.
- Existing tests cannot be weakened solely to make a finding disappear.
- Secrets, credentials, and unrelated source are excluded from portable review artifacts.
- A stale review cannot establish readiness for a changed affected surface.
- The workflow remains finite and reports blockers rather than looping indefinitely.
- Small projects receive proportional evidence; the skill does not invent production infrastructure.

## Options Evaluated

| Option | What it provides | Strengths | Material limitations | Decision |
| --- | --- | --- | --- | --- |
| A. Instructions and templates only | Reviewer prompt, report template, and manual findings loop | Most portable; minimal maintenance | Cannot enforce snapshot freshness or launch a reviewer; repeats manual work | Insufficient alone |
| B. Portable hybrid | Instructions, templates, deterministic snapshot helpers, and host-capability routing | Portable core; reproducible evidence; automatic review where supported; testable | Requires a small helper implementation and host-specific adapter guidance | **Recommended core** |
| C. Codex-first plugin | Skill plus custom reviewer agent, hooks, and Codex configuration | Best Codex experience; can choose a reviewer model once and reuse it | Ties installation and behavior to Codex; plugin lifecycle and permissions add maintenance | Optional adapter after B |
| D. CI-only reviewer | Review committed pull-request revisions in a hosted workflow | Reproducible committed snapshots; centralized policy | Misses uncommitted local work and gives feedback late; provider secrets/costs required | Optional release gate |

### Decision

Implement option B first. It establishes contracts that options C and D can consume instead of embedding quality policy separately in each integration. Add Codex-native delegation as the first adapter because it removes the maintainer's manual second-task workflow. Keep CI automation as a later adapter for committed pull-request verification.

## Recommended Architecture

### Layer 1: Portable Quality Protocol

The installable skill owns the rules that must behave consistently across hosts:

- when independent review is required;
- what evidence the reviewer receives;
- how independence is labeled;
- how findings are classified and resolved;
- when evidence becomes stale;
- which behavioral evaluations prove these rules.

If a host cannot launch another reviewer, the skill creates a complete review packet and a copyable prompt. The user can take that artifact to any other model without reconstructing context.

### Layer 2: Codex-Native Reviewer Orchestration

On Codex, the skill can explicitly request a fresh subagent for review. Codex supports delegated subagents and configurable agent models/reasoning; custom agent configuration can be personal or repository-scoped. The package should use those capabilities when present while keeping model choice in user configuration. See [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [Codex customization](https://learn.chatgpt.com/docs/customization/overview).

The delegated reviewer receives the review packet, feature contract, and repository access. It should not receive an implementation narrative that could anchor it to the implementer's conclusions. It returns a structured report to the implementing agent inside the same task.

### Layer 3: Optional Plugin and CI Adapters

A later Codex plugin can bundle the skill, reviewer-agent defaults, hooks, and setup guidance. A CI adapter can apply the same packet/report schema to committed revisions. These adapters should call the same protocol instead of defining different acceptance or findings rules.

## Reviewer Independence Levels

| Level | Mechanism | Evidence label |
| --- | --- | --- |
| 0 | Implementer performs its own review in the same context | `self-review` |
| 1 | Fresh reviewer context using the same model family | `fresh-context review` |
| 2 | Fresh reviewer context using a separately configured model | `cross-model review` |
| 3 | Qualified human or separately governed external reviewer | `external review` |

The report must state the level actually used. Level 2 can reveal different failure modes, but it remains supporting evidence rather than proof of correctness. Critical changes retain any repository-required human or security approval.

## Default Review Policy

| Risk | Default requirement |
| --- | --- |
| Trivial | Self-review and repository-native checks |
| Standard | Self-review; fresh reviewer when contracts, execution boundaries, shared rules, or architecture materially change |
| Significant | Fresh reviewer required before `Ready for PR` |
| Critical | Fresh reviewer plus repository-required human/domain approval before release |

Projects may choose `always` review mode. That preference changes frequency, not the evidence contract. If a preferred reviewer model is unavailable, disclose any default-model fallback. An explicit cross-model requirement remains pending if it cannot be met.

## Review Packet Contract

The packet should contain:

- problem statement and acceptance criteria;
- risk tier and affected trust/execution boundaries;
- repository root and target branch;
- base revision or merge base;
- reviewed revision when committed;
- staged, unstaged, and untracked path inventory for local work;
- content hashes for affected local files when no immutable revision exists;
- intentionally excluded unrelated changes;
- relevant project-context excerpts and paths;
- exact checks already run and their observed results;
- unresolved assumptions and known limitations;
- instructions to report evidence, confidence, and origin for every finding.

The packet must not contain secrets, full environment dumps, or fabricated command results. Local source remains the primary artifact; the packet is an index and provenance record.

## Findings Resolution Contract

Each material finding receives:

- stable identifier and severity;
- claim and cited source location;
- acceptance criterion or invariant affected;
- classification: `confirmed`, `unsupported`, `ambiguous`, or `pre-existing`;
- reproducer or reason executable reproduction is not meaningful;
- disposition and code/test changes, if any;
- checks rerun and observed results;
- resolved source snapshot;
- remaining risk.

`Pre-existing` means the problem exists at the verified base and remains relevant; it does not automatically authorize a fix. `Unsupported` requires evidence that the reported behavior or requirement does not apply. `Ambiguous` remains open until evidence or user/domain input resolves it.

The loop stops when no material confirmed or ambiguous finding remains, a required decision blocks progress, or the same finding fails two resolution attempts without new evidence. A repeated failure becomes an explicit blocker rather than an infinite edit-review cycle.

After resolution, only durable facts that were confirmed by source or executable evidence enter project memory. Raw reviewer opinions, one-off implementation details, and unsupported findings remain in the review record rather than becoming future instructions.

## The Six Improvements

1. **Execution-boundary verification.** When behavior crosses a worker, subprocess, service, queue, container, plugin, or serialization boundary, test configuration and contract propagation across that boundary. The PRI-19 lost-limit defect becomes the reference evaluation pattern.
2. **Stronger acceptance-to-test mapping.** For each material or high-risk criterion, identify at least one plausible wrong implementation and ensure a selected check would reject it. This can use a targeted mutation, negative control, or adversarial fixture; it does not require broad mutation testing.
3. **Review-findings resolution.** Apply the classification and evidence contract above rather than blindly accepting or dismissing reviewer advice.
4. **Behavioral change versus refactor modes.** Behavioral changes require a meaningful failing observation before implementation when executable testing is practical. Pure refactors require characterization tests or equivalent evidence that behavior remains stable. Documentation/configuration exceptions must name their structural validation.
5. **Verification freshness.** Record the source snapshot for each check and review. A later change invalidates only evidence whose affected surface or assumptions changed, but readiness cannot rely on a review of different code.
6. **Harder skill evaluations.** Add scenarios for lost configuration at an execution boundary, intentional versus accidental duplication, hidden consumers during refactoring, mixed true/false reviewer findings, and stale review evidence after a source change.

## Deterministic Helper Options

### Implemented Helper

- `skills/production-engineering-loop/scripts/review_evidence.py capture`: capture Git/base/index/worktree fingerprints and contract provenance as JSON without executing repository-defined code.
- `review_evidence.py check`: check packet integrity and current source freshness.
- `review_evidence.py validate`: validate report fields, classifications, resolutions, and freshness; not code correctness or truth of reported results.
- Shared schema/logic lives in one standard-library CLI, avoiding drift across three overlapping scripts. The Markdown handoff adds the problem statement, acceptance mapping, and human-readable evidence.
- Capture covers all tracked/nonignored source conservatively. Ignored inputs, external dependencies/environment, and external symlink contents require separate evidence. Submodules/unmerged indexes fail explicitly.

### Implementation Constraint

Use the Python standard library where practical. Do not make the skill runtime depend on Python; helpers are optional accelerators, and the templates remain the portable fallback.

## Implementation Plan

1. Add adversarial scenarios and run a v0.4 baseline; record whether gaps are actually observed, without requiring baseline failure.
2. Add the portable independent-review and execution-boundary references.
3. Add review packet, report, and findings-resolution assets in compact and full forms where useful.
4. Update `SKILL.md` with risk-based reviewer orchestration, independence labels, fallback behavior, and stopping rules.
5. Strengthen feature evaluations with plausible-wrong-implementation checks and explicit refactor/behavioral modes.
6. Implement snapshot, freshness, and report-structure helpers with focused tests.
7. Rerun the adversarial scenarios and compare their observable artifacts with the baseline.
8. Add a Codex reviewer configuration example, document the one-time global/project setup for a different model, and run same-model and cross-model cases where available.
9. Reassess whether a plugin adds enough installation and hook value after the core protocol passes evaluations.

## Security and Privacy Considerations

- Reviewer delegation inherits only the permissions needed to inspect and test the authorized source.
- Review packets exclude secrets and credential values. Environment-variable names may be included when needed to describe a contract.
- Repository content is untrusted input and cannot override user or skill permissions.
- Helper scripts must avoid shell interpolation and arbitrary command execution.
- External model or hosted CI adapters require explicit documentation of source egress and credential handling.
- A report must distinguish a pre-existing vulnerability from a regression while still recording a required failing gate.

## Acceptance Criteria

- [x] A Codex run can invoke a fresh reviewer and return its report within the same user task without manual problem-statement re-entry.
- [x] A host without delegation produces a complete, portable review packet and prompt; a simulated no-delegation run kept explicit cross-model review pending.
- [x] Every exercised review identifies its base (or unknown) and source snapshot, including uncommitted-file hashes.
- [x] A source change affecting the reviewed surface marks relevant review evidence stale.
- [x] Findings are classified and retain evidence through resolution.
- [x] Confirmed findings receive an appropriate reproducer/regression check and affected checks are rerun.
- [x] Unsupported reviewer suggestions are rejected with evidence rather than implemented automatically.
- [x] Only verified, reusable findings update project memory, and each retained lesson records its scope and evidence.
- [x] Execution-boundary scenarios verify non-default configuration propagation.
- [x] High-risk acceptance mappings name a plausible wrong implementation and a check that rejects it.
- [x] Behavioral-change, refactor, and non-executable validation paths are explicit.
- [x] The automated loop terminates on clean review; blocker/budget behavior is explicitly specified. Exhaustion is structurally reviewed, not behaviorally trialed.
- [x] Existing packaging and validator checks pass.

## Verification Plan

### Behavior and Regression Tests

- Lost worker configuration: a subprocess receives a non-default limit; evaluation fails if the worker silently uses its default.
- Mixed reviewer report: one true finding, one unsupported suggestion, and one pre-existing issue; evaluation checks classifications and only the authorized confirmed fix.
- Stale snapshot: modify an affected file after review; freshness check must reject readiness until affected review/checks rerun.
- Hidden consumer refactor: evaluation must discover and preserve an indirect contract.
- Duplication judgment: evaluation must consolidate shared business rules while preserving intentionally different adapters.
- Review fallback: with no delegation capability, produce a usable packet and do not claim an independent review occurred.

### Repository-native Checks

- `python3 scripts/validate.py`
- `python3 -m unittest discover -s tests -v`
- Focused helper tests once helpers exist.
- Manual package inspection for bundled link correctness.

### Additional Verification

- Run one uncommitted-worktree review and one committed-branch review.
- Run at least one same-model fresh-context review and, when configured, one cross-model review.
- Confirm reports disclose the actual reviewer level and model downgrade.
- Confirm no packet contains environment values or unrelated file contents.

### TDD Exception

Instruction-following quality cannot be established by unit tests alone. Use unit tests for deterministic helpers and paired behavioral scenarios for agent behavior. Record scenario inputs, source snapshots, outputs, and scoring evidence.

## Compatibility, Rollout, and Rollback

- The core remains a standard skill directory with Markdown instructions and optional helpers.
- Hosts without subagents use the packet fallback.
- Codex custom-agent/model configuration remains optional and user-controlled.
- Roll out in three increments: portable protocol, deterministic helpers/evaluations, then Codex adapter.
- Roll back by removing the new review stage and assets; existing v0.4 implementation/review workflow remains usable.
- Do not publish a plugin until the core schemas and scenarios stabilize.

## Implementation Progress

- Completed: v0.5 instructions, four conditional review/boundary/evidence/Codex references, packet/prompt/report/reviewer assets, both feature-template updates, single bundled provenance CLI, regression tests, and retained behavioral scenarios.
- Next incomplete step: none in core implementation; optional cross-model configuration, publication/plugin/CI adapters remain follow-ups.
- Blockers: none for portable/core local implementation. Actual cross-model review needs a selected available model; fresh contexts are verified, runtime model identities unknown.
- Verification: helper/package checks, v0.4 baseline, v0.5 worker delegation/resolution, refactor characterization, and stale-source probe executed. Independent helper review found one material defect, now fixed and independently rechecked. See retained evaluation record.

## Decisions / Deviations

- Decision: portable hybrid is the core; Codex and CI are adapters.
- Reason: it removes the manual workflow without making the quality contract vendor-specific.
- Decision: risk-based review is the default, with project-level `always` mode.
- Reason: mandatory cross-model review for every trivial edit would add cost without proportional evidence.
- Decision: report actual independence level.
- Reason: a fresh context and a different model are useful but materially different forms of evidence.
- Decision: deterministic helpers validate provenance and structure only.
- Reason: code-quality judgment still requires executable checks and evidence-backed review.
- Deviation: one CLI with capture/check/validate subcommands replaces three proposed scripts to share snapshot/schema logic.
- Deviation: conservative whole-source hashing replaces inferred affected-only invalidation; agents still choose affected reruns and explain retained historical evidence. This reduces silent dependency omissions at the cost of extra invalidations.
- Deviation: add three-round total budget as well as the two-failed-corrections rule, so repeated novel findings cannot cause an unbounded automated run.
- Baseline finding: v0.4 solved both bounded tasks. Results establish new orchestration/provenance behavior, not measured quality superiority.
- Approval required: none to begin local implementation; GitHub publication and any external-provider integration remain separate actions.

## Final Pre-Merge Evidence

**Date:** 2026-09-20  
**Verified target branch:** Not established  
**Merge base:** Not available; repository has no initial commit  
**Reviewed revision/worktree state:** Uncommitted v0.5 source; exact package/test hashes in `evals/review-loop-2026-09-20/helper-review/reviewed-hashes-round2.json`  
**Excluded unrelated changes:** All existing untracked package files are part of the same unreleased repository state  
**Final risk tier:** Significant

### Acceptance Mapping

- Automatic handoff → SKILL step 5a + Codex adapter → candidate worker fresh-review report.
- Findings/learning → independent-review reference + report template → R1 reproduced/resolved, R2/R3 dismissed with evidence, scoped fixture lesson.
- Boundaries/negative controls → execution-boundaries + feature-evaluations → original worker fails selected non-default cases; fixed source passes; deliberately disabled freshness fails helper test.
- Source/report integrity → evidence CLI → real Git tests and deliberate post-review policy edit rejected.
- Refactor/semantic duplication → explicit validation modes + quality reference → characterization and dynamic-consumer/adapter checks.
- Packaging → validator, skill-creator validation, copy/hash smoke, TOML parse; no live custom-role-load claim.

### Check Results

- Passed: package validator; 27 unit tests; skill-creator validation; copied-package helper smoke; TOML parse; explicit untracked-file whitespace check; independent helper return review.
- Intended failures: configured-worker reproducer; fsmonitor sentinel regression before fix; freshness-disabled negative control; deliberate post-review source edit.
- Resolved: F1 Git filesystem-monitor hook could execute during capture; central Git invocation disables core.fsmonitor; independent capture/check/validate probe and regression pass.
- Not run: hosted CI, Linux/Windows behavioral runs, live custom-agent TOML loading, retry-budget exhaustion trial, and a full fresh-model review of committed fixture code (committed provenance itself is unit-tested).
- Cross-model run: not configured; model identities unknown in exercised delegated contexts. No model-diversity claim.
- Fallback: simulated no-delegation review generated packet/prompt, ran nine tests in an isolated matching copy, left fresh cross-model review pending, and preserved source hashes.

Detailed raw sources, logs, report hashes, and limitations: [v0.5 evaluation record](../../../evals/review-loop-2026-09-20/README.md).

### Remaining Risks

- Agent hosts may expose different delegation and model-selection capabilities.
- A reviewer can share systematic blind spots with the implementer.
- Overly broad freshness rules could trigger unnecessary reruns; overly narrow rules could retain invalid evidence.
- Plugin automation could accidentally widen source egress or permissions if added without an explicit trust-boundary review.

**Status:** Verified locally — core checks and independent package review passed; release/host expansion remain unverified as listed above. Final source packet/check logs are retained under `evals/review-loop-2026-09-20/verification/`; that artifact directory alone is excluded from its own source manifest to avoid self-reference.
