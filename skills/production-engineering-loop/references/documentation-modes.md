# Compact and full documentation

Select documentation depth separately from engineering quality. Both modes require an understood contract, justified design, relevant source/caller inspection, meaningful validation, and an honest handoff. A shorter record is not permission to skip work. Do not grade quality by document length.

## Choose a mode

| Mode | Default use | Record |
| --- | --- | --- |
| Compact | Bounded bug fix, small feature, or behavior-preserving refactor inside understood boundaries; usually Standard risk | Existing issue/feature record or [compact template](../assets/feature-compact-template.md) |
| Full | Significant/Critical risk, new subsystem or architecture, public/shared contract changes, migrations, or substantial coordination across features | Existing equivalent specification or [full PRI template](../assets/feature-template.md) |

Trivial nonbehavioral edits can use the task response and relevant check result; do not create a feature document just to fill a template. For a small greenfield program, briefly establish responsibilities before choosing a mode; being new does not by itself require enterprise layers or extensive paperwork. Choose full when unresolved architecture or boundaries require a substantive design decision.

State the chosen mode and reason briefly in the record. Reuse the current feature record rather than creating parallel compact and full versions. If the user supplies a full PRI contract, preserve its sections and requirements; maintain a compact Execution Context at the top for navigation. Do not silently convert it to the compact template. An explicit request for a compact format governs presentation even for risky work; include all applicable risk, design, security, compatibility, and recovery evidence in that record or linked canonical sources.

## Information both modes retain

- Goal, acceptance criteria, scope, invariants, and material failure cases.
- Risk and affected boundaries, including consumers beyond the edited file.
- Current source locations and the next incomplete step, with freshness evidence.
- Design basis: existing pattern and canonical rule locations, or a justified new responsibility/interface; meaningful duplication and dependency decisions.
- Criterion-to-check mapping, exact commands/procedures, actual results, and missing evidence.
- Actual changed files, unresolved findings, compatibility effects, and a scoped lesson when supported.

Link existing decisions, project maps, and evidence rather than copying them. Compact mode can express these in a few bullets and a small acceptance table. Full mode expands the detail required by the supplied PRI structure. Neither requires an empty checklist of unrelated technologies.

## Escalate when the work changes

Reassess risk and documentation when investigation uncovers additional consumers, incompatible behavior, a trust boundary, shared state, or a rollout/recovery dependency. By default, expand a compact record to full when its conditions apply. Preserve criterion IDs, decisions, completed evidence, and user-authored requirements. If an explicitly requested compact format remains in use, expand its relevant content and link detail; never omit obligations to fit a length target.

Changing documentation depth is routine work within an authorized task. A change in product scope or an irreversible action still needs the corresponding authority. Do not ask for permission merely to write the appropriate record.

## Keep current context distinct from history

Keep the current goal, locations, decisions, verification state, and next step easy to find. Label older runs with their source snapshot and move long historical detail to existing evidence/archive locations when useful. Preserve evidence and links; do not delete relevant requirements or claim an old pass applies to new code. For review-only work, use existing documents and propose updates in the response without writing files.

## Examples

- **Compact:** correct a local parser's empty-input handling. Identify the parser/callers, preserve the error contract, add a failing behavioral case, implement, review, and record actual checks.
- **Compact:** add a small operation using an existing domain policy and adapter. Record why the policy is reused and verify both success and boundary failure paths.
- **Full:** change a shared API's pagination contract. Map clients, compatibility, migration strategy, integration cases, and rollback alongside the implementation plan.
- **Full:** introduce persistence into a project with no established storage boundary. Define ownership, failure semantics, data integrity, and justified dependency direction before implementing.

The distinction is the amount of coordination and evidence to explain, not whether the developer values quality.
