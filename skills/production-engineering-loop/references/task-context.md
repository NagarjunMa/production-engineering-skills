# Feature context and focused retrieval

Use when defining a feature contract, resuming partially completed work, or locating code for a substantive task. Choose [compact or full documentation](documentation-modes.md). The full template preserves the PRI-style problem, scope, risk, plan, acceptance, verification, progress, and pre-merge sections. Its Execution Context is a concise entry point into that contract and the current source; the compact template provides the equivalent current context in fewer sections.

## Three layers of context

1. **Project map:** product intent, stack, subsystem responsibilities, feature links, and repository-wide commands. Read the compact summary and relevant entries; do not load every feature or lesson.
2. **Feature contract:** requested outcome, boundaries, invariants, risks, decisions, and evaluation requirements. Read the current contract when taking ownership, including constraints outside Execution Context. A summary cannot override or silently omit a requirement.
3. **Code locations:** concrete paths, symbols/routes, relevant callers, test entry points, and focused checks for the next incomplete step. Open the actual code and necessary surrounding logic before modifying it.

Keep one canonical record for each fact. The project map links features; the feature record links code. Do not copy whole source files, directory trees, CI logs, or every architecture decision into task documents. Preserve a user-supplied contract's headings and requirements; add or maintain the location map without replacing the contract with a shorter summary.

## Build the location map once

Inspect existing source and repository conventions to populate repository-relative paths and durable symbols. Classify each location as:

- **Verified:** file/symbol and relevance inspected at the recorded source snapshot.
- **Candidate:** plausible location found by search or supplied by the user, not yet verified.
- **Planned:** a proposed new file; placement and responsibility are not implemented facts.

Record each location's role (edit/read/test/config), why it matters, and the intended action. Include relevant callers, shared contracts, data access/authorization boundaries, representative maintained implementations, and existing regression tests. Avoid listing unrelated files merely because a search matched their names.

Prefer path/module lookup first, then symbol or route queries inside the relevant subsystem. Widen progressively if needed. A repository-wide file-name or symbol lookup can be cheaper than guessing; distinguish that lookup from loading every matching file into context. Dynamic registration, framework conventions, generators, and public consumers may require broader tracing than text search alone.

Use symbols as anchors rather than permanently trusting line numbers. Include scoped repository instructions for mapped paths. Verify exact check commands, working directories, runtime constraints, and required CI jobs from repository configuration; do not infer availability from the language or framework.

## Start or resume

1. Read applicable instructions, the active contract, and Execution Context. Find the next incomplete step and its acceptance criterion.
2. Inspect current worktree state and the map's source snapshot. Include uncommitted/untracked files; preserve user edits and do not assume HEAD represents the workspace.
3. Confirm paths and symbols exist. Compare relevant source, manifests, test configuration, and dependency boundaries with the recorded evidence. If the old revision is unavailable, treat the map as a lead and revalidate relevant locations.
4. Open mapped implementation, tests, callers, and contracts needed for that step. Read coherent functions/classes and necessary context, not snippets that hide error handling or side effects.
5. Reconcile completed work with code and evidence. Do not redo finished work or trust a stale progress checkbox as proof of completion.
6. Execute the scoped increment and checks. Broaden investigation when evidence requires it, then refresh the map for the next session.

On resume, use the next step, relevant decisions, and evidence references. Read changed contract sections and referenced constraints; if prior understanding is unavailable or uncertain, reread the active contract. Never save tokens by skipping security/privacy requirements, invariants, or required checks.

## When to broaden inspection

Expand when a path is renamed, a symbol is absent, an interface or dependency changes, a helper has additional consumers, a check points elsewhere, or a new trust boundary appears. Explain the concrete reason. Update the risk tier and seek a missing product/scope decision only when needed; discovering more callers is not automatic permission to modify them all.

“Areas not needed initially” are retrieval hints, not an absolute prohibition on relevant inspection. Explicit user edit restrictions remain binding. If required source is inaccessible, report that limitation.

## Keep handoffs short and fresh

At meaningful checkpoints refresh current status, next step, changed locations, actual file actions, check evidence, and unresolved gaps. Do not append a narrative of every command. Label historical results with their tested snapshot and link evidence where available.

Do not assume an issue number, target branch, merge base, or owner. Use verified task/repository evidence; otherwise mark unknown or unassigned. Approval fields document real boundaries rather than adding confirmation for routine authorized work.

Use the supplied template's red/green sequence when meaningful: add/update the regression case, observe the intended behavioral failure, implement, then refactor with checks green. A test-collection error or missing dependency does not establish the intended red state. Record a TDD exception only when executable tests are not meaningful; missing tools remain a blocker. Follow stronger explicit repository/user testing rules.

## Optional context-efficiency evaluation

The primary goal is informed, high-quality implementation. Context efficiency is secondary and does not determine whether a necessary inspection or check is performed.

Savings should come from avoiding repeated discovery and irrelevant code loading; no fixed percentage is guaranteed. Compare matched runs with and without a verified context map. Record files/bytes read, repeated reads, unrelated areas loaded, available token counts, elapsed time, and actual correctness. File-read counts are proxies, not token measurements.

Include stale-map and incomplete-map scenarios. A successful agent narrows fresh-context work but expands when needed, preserves requirements, and passes relevant evaluations. Fewer reads with a missed caller, weakened test, or wrong change is a failure. Initial mapping costs work; assess whether later tasks recover that cost.
