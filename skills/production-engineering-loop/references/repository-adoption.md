# Repository Adoption

Adopt the loop as layered controls: repository-owned instructions for shared judgment, automated checks for deterministic requirements, and human review for product and high-risk decisions.

## Keep Ownership Explicit

A personal skill is an engineer-level aid, not a repository dependency. Do not make CI, hooks, or shared repository instructions depend on a path under a contributor's home directory.

- Keep personal skills under the agent's configured personal skill directory.
- Put every mandatory team rule in a repository-owned `AGENTS.md` or engineering guide so collaborators and CI have the same source of truth.
- Vendor a skill into a repository only after an explicit team or distribution decision. Do not vendor it merely because one engineer uses it locally.
- Keep repository validators self-contained and read-only; they must not inspect personal agent state.

The personal skill may remind an agent to apply the repository policy, but the repository policy must remain understandable and enforceable without that skill.

## Shared project knowledge

Reuse the team's product, architecture, decision, and feature documentation for persistent context. When no equivalent exists, use the skill's default `docs/engineering-loop/` structure and templates. Keep the project map compact, feature evaluations tied to requirements and tested revisions, and lessons supported by evidence. Store these records with the project so another tool or contributor can use them. Keep secrets and private transcripts out of them.

Knowledge records describe observed state and decisions; they do not override repository policy, current user instructions, or source evidence. Resolve drift and conflicting updates as part of the relevant task. Do not require all developers to use this skill to understand or maintain the records.

## Deterministic Enforcement

Inventory package scripts, hooks, CI workflows, protected branches, coverage rules, security scanners, migration checks, and release jobs before adding anything.

- Enforce formatting, linting, type checking, tests, builds, schema validation, artifact integrity, and security scans in tooling where the answer is deterministic.
- Establish a passing baseline before making a new check required. Track existing failures separately rather than adding a permanently failing or silently skipped gate.
- Keep local hooks fast enough to be used. Put expensive or environment-specific validation in CI or an explicit pre-release workflow.
- Use a read-only policy-integrity check when accidental removal of mandatory instructions or review evidence is a credible regression.
- Configure important CI jobs as required branch checks; a workflow that runs but is not required can still be bypassed during merge.

Automation proves only the condition it checks. Do not label a marker, checklist, or policy-file validator as proof that the engineering review itself occurred.

## Pull Request Evidence

Provide stable sections for:

- acceptance criteria and risk tier;
- affected boundaries and data;
- commands, results, and measurements;
- security, privacy, and data-integrity findings;
- compatibility, migration, rollout, and rollback;
- regression risks and mitigations;
- remaining risks and follow-up owners.

Allow concise `N/A` entries with reasons. Avoid requiring ceremonial prose or exact generated wording.

## Rollout

1. Install the personal skill for engineers who want it and add a self-contained repository policy for mandatory behavior.
2. Validate both independently and run the repository's existing required checks.
3. Dogfood the process on representative feature, fix, and configuration or schema changes.
4. Record confusing, redundant, or missed decisions and narrow the workflow based on observed failures.
5. Publish or broaden adoption only after the workflow is useful without causing repeated irrelevant work.
