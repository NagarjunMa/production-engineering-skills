# Production Engineering Loop

**Build maintainable code. Verify its behavior. Carry that discipline between projects.**

A portable skill for AI coding agents that turns implementation into a bounded loop:

```text
Read problem + project memory → Inspect source → Define feature evaluations
         ↑                                                 ↓
Update project map + lessons ← Verify ← Review ← Implement / fix
                               Stop when the contract is met.
```

Use it to build features, fix bugs, review changes, and refactor existing code. It starts from the problem statement and the relevant source, retains verified project knowledge across tasks, scales scrutiny to risk, and requires evidence before claiming success. It works with new or existing projects, with or without a formal implementation plan, commit, branch, or GitHub repository.

## What is this skill?

Production Engineering Loop is a reusable instruction package for AI coding tools. It gives the coding agent an engineering workflow, supporting references, feature templates, review instructions, and an optional source-evidence helper.

It is not a code generator, framework, background service, or replacement for the model in your coding tool. The host agent still reads and edits the project using its existing tools and permissions. This skill tells that agent how to investigate the request, preserve the project's architecture and contracts, implement the change, evaluate it, review it, and report what was actually verified.

The workflow is language independent. It can be used for a small personal application, an early-stage product, a library, or an established production codebase.

## Why was it created?

AI coding tools can produce code quickly, but speed alone does not protect a project from locally correct changes that break another caller, duplicate an existing rule, introduce an unnecessary abstraction, weaken a test, or drift away from the codebase's established design.

The skill was created to make the quality process repeatable across multiple projects and coding sessions. It addresses four recurring problems:

- Agents often start a task without a durable map of the product, stack, important files, contracts, and prior decisions.
- A feature can appear complete even when failure paths, compatibility, security boundaries, or affected consumers were not evaluated.
- Review findings can become detached from the exact source that was reviewed, especially after more edits are made.
- Useful lessons from one feature are frequently lost, forcing later sessions to rediscover the same architecture and constraints.

The primary goal is better code: correct behavior, sound architecture, cohesive modules, consistent business rules, and evidence-backed completion. Faster delivery and reduced repeated discovery are useful secondary effects, but the skill does not reduce quality work merely to save tokens.

## What does it do?

For a substantive development or review task, the skill guides the agent through this loop:

| Stage | What the agent does |
| --- | --- |
| Understand | Reads the problem statement, repository instructions, relevant project records, active changes, and source boundaries. |
| Map | Identifies the stack, important files, responsibilities, callers, shared contracts, and areas that were not inspected. |
| Contract | Defines the intended behavior, non-goals, invariants, risk, acceptance criteria, and suitable verification. |
| Evaluate first | Selects behavioral cases and material failure paths that could distinguish a correct implementation from a plausible wrong one. |
| Implement | Follows sound existing patterns or introduces the smallest useful modular boundary when the project has no established pattern. |
| Verify | Runs repository-native tests and checks, records exact results, and distinguishes passed, failed, skipped, blocked, and unexecuted evidence. |
| Review | Examines correctness, affected consumers, compatibility, modularity, duplication, patterns, security/privacy, and verification integrity. |
| Resolve | Verifies reviewer findings, fixes confirmed in-scope problems, adds regression evidence where useful, and reruns affected checks. |
| Retain | Updates compact project and feature records with current paths, decisions, results, limitations, and reusable lessons. |

The developer chooses the source to evaluate: active uncommitted work, staged changes, a branch or revision range, selected files or subsystems, or completed existing code. The skill never requires a commit, push, pull request, or GitHub workflow.

It also supports distinct working modes:

| Intent | Behavior |
| --- | --- |
| Implement and review | Build the requested change, verify it, review it, and resolve supported findings. |
| Review only | Inspect and report without editing the source or external systems. |
| Review and fix | Confirm reported problems, correct the in-scope findings, and rerun relevant checks. |
| Behavior-preserving refactor | Improve structure while characterizing and preserving required behavior. |
| Project onboarding | Map the product, stack, architecture, important files, risks, and inspection gaps before later feature work. |

## What it does not promise

This skill does not guarantee perfect or vulnerability-free code, certify compliance, replace required human review, make deployment decisions, or prove that a reported test actually ran. Model capability, repository context, available tools, permissions, tests, and reviewer judgment still determine the outcome.

It does not retrain the model or silently modify itself. Its “self-improving” loop improves repository knowledge, feature evaluations, and regression evidence after observed outcomes. It does not run in the background or automatically create a backlog.

## Install for a new user

The complete installable package is the [skills/production-engineering-loop](skills/production-engineering-loop/SKILL.md) folder. It contains the skill entrypoint, supporting references, templates, optional evidence helper, Codex UI metadata, an optional reviewer-role example, and the license. Repository-level tests, evaluation artifacts, and development documentation are not runtime dependencies.

The package uses the open [Agent Skills format](https://agentskills.io/specification). Normal use requires no API key, MCP server, background service, installation hook, Python runtime, or GitHub account. The command-line installer requires Node.js/npm. Git and Python 3.10+ are needed only if the agent uses the optional source-evidence helper.

### 1. Choose the installation scope

| Scope | Choose it when | Result |
| --- | --- | --- |
| Personal/global | You want the skill available in all of your local projects | Installed in the coding tool's personal skills directory |
| Project | A team or one repository should use and version the skill | Installed under the current project's supported skills directory |

Avoid installing both personal and project copies unless you intentionally need different versions. Multiple discoverable copies can make it unclear which instructions the agent loaded.

### 2. Install from GitHub

After this repository has a public owner, replace `YOUR_GITHUB_OWNER` in these commands.

Personal installation for Codex:

```sh
npx skills add YOUR_GITHUB_OWNER/production-engineering-loop \
  --skill production-engineering-loop --agent codex --global --yes
```

Project installation for Codex, run from the target project's root:

```sh
npx skills add YOUR_GITHUB_OWNER/production-engineering-loop \
  --skill production-engineering-loop --agent codex --yes
```

For another supported tool, replace `codex` with the agent identifier supported by the [Skills CLI](https://github.com/vercel-labs/skills), or let the installer prompt you to choose. Exact discovery and invocation behavior belongs to the host tool.

### 3. Install from a local clone

To test or develop the skill before publication:

```sh
npx skills add /absolute/path/to/production-engineering-loop \
  --skill production-engineering-loop --agent codex --yes
```

Add `--global` when you want that local installation available across projects.

### 4. Install manually when needed

Copy the **whole** `skills/production-engineering-loop` directory into the host's personal or project skills directory. Do not copy only `SKILL.md`; its references, templates, license, helper, and metadata are part of the package.

For Codex:

| Scope | Destination |
| --- | --- |
| Personal | `~/.agents/skills/production-engineering-loop/` |
| Project | `<project>/.agents/skills/production-engineering-loop/` |

The [installation and compatibility guide](docs/installation.md) contains Windows instructions, directories for Claude Code, Cursor, GitHub Copilot, and Gemini CLI, update/removal guidance, and a file-based fallback for tools without native skill support.

### 5. Confirm the installation

1. Restart or reload the coding tool if it does not refresh skills automatically.
2. Open the tool's skill list and confirm that **Production Engineering Loop** appears once and is enabled.
3. Start with an explicit, bounded request so activation is unambiguous.

For Codex:

```text
Use $production-engineering-loop to review the current uncommitted changes.
Do not edit files. Check behavior, affected callers, modularity, duplication,
and the relevant tests. Report exact evidence and remaining limitations.
```

Installation proves that the host can discover the package. It does not by itself prove that every model will follow every instruction correctly. Evaluate a known task and inspect the resulting plan, changes, checks, and review evidence.

## Use it on real work

Explicitly name the skill and describe the outcome and constraints. You can supply a short task, an issue, or the full PRI-style template bundled with this project.

Implementation example:

```text
Use $production-engineering-loop to implement cursor pagination for GET /orders.
Preserve the existing response fields and authorization behavior.
Define the acceptance and failure cases, implement the change, run the relevant
repository checks, review the result, and resolve confirmed findings.
```

Project onboarding and implementation example:

```text
Use $production-engineering-loop to read this problem statement and inspect the
relevant codebase. Record the product, stack, architecture, file responsibilities,
and inspection gaps. Define evaluations for the requested feature, implement it,
and update the project records with actual results.
```

Review-and-fix example:

```text
Use $production-engineering-loop to review the current branch against this problem
statement. Verify each finding against the current source, fix confirmed in-scope
issues, add regression coverage where appropriate, and rerun affected checks.
```

In Claude Code, invoke `/production-engineering-loop` followed by the task. In other tools, select the installed skill or ask the agent to read its `SKILL.md`. Automatic invocation depends on the host; explicit invocation is preferable for the first test.

A useful handoff might look like this **illustrative example**, not a result from this repository:

> Implemented the pagination fix while preserving the response shape. Significant risk: public API contract. Passed: focused pagination tests and type checks. Integration tests were blocked by an unavailable local database. Implementation is complete; integration verification remains pending.

## How much process does it add?

Choose [compact or full documentation](skills/production-engineering-loop/references/documentation-modes.md). Both modes retain the same applicable engineering checks; document length does not set the quality bar.

| Mode | When to use | What changes |
| --- | --- | --- |
| Compact | Bounded fixes, small features, local refactors in understood boundaries | Short contract, relevant design decisions, acceptance evidence, and handoff in an existing record or the compact template |
| Full | Significant/critical risk, substantial features, new architecture, shared contracts, migrations | Complete PRI structure with expanded boundary, design, verification, and delivery detail |

Explicit user-supplied documents and requirements are preserved. Both modes review architecture fit, relevant redundancy, modularity, failure paths, and affected callers. Critical changes require additional review before release. A skill does not grant deployment authority or replace your repository's required checks.

The [main skill](skills/production-engineering-loop/SKILL.md) contains the loop. Supporting references cover [project learning](skills/production-engineering-loop/references/project-learning.md), [feature evaluations](skills/production-engineering-loop/references/feature-evaluations.md), [risk tiers](skills/production-engineering-loop/references/risk-tiers.md), [code quality](skills/production-engineering-loop/references/code-quality-review.md), [JavaScript/TypeScript](skills/production-engineering-loop/references/javascript-typescript.md), and [team adoption](skills/production-engineering-loop/references/repository-adoption.md). The core workflow is language independent; the JavaScript/TypeScript reference is optional.

## Automatic review and resolution (v0.5)

For significant changes and changes to shared rules or execution contracts, the skill asks a capable host to launch a fresh reviewer inside the current task. It supplies the requirements, source snapshot, and review prompt, verifies returned findings, fixes confirmed issues within scope, reruns affected checks, and obtains a return review. There is no manual second-chat handoff in a host that supports this workflow. Set an `always` review preference in your task or existing project instructions to apply it to smaller changes too.

The default is at most three reviewer rounds, with an earlier stop after two unsuccessful corrections of the same finding without new evidence. Unresolved findings remain pending when the budget expires. Review-only requests stay read-only. Required cross-model/human review cannot be replaced by self-review.

Hosts without delegation receive a portable packet and reviewer prompt; required independent review remains pending. Fresh same-model review and known cross-model review are labeled separately. A skill requests this behavior; host capabilities, permissions, and model instruction following determine execution. It is not a background service or an enforced merge gate.

The bundled [evidence helper](skills/production-engineering-loop/references/review-evidence.md) uses Python 3.10+ and Git to capture committed or uncommitted source fingerprints, detect staleness, and validate report structure. Its Git processes are forced offline; missing promised objects stop capture instead of being downloaded. It does not verify that reported tests truly ran or decide whether code is correct. Python and Git are optional for manual/template use. The [Codex adapter](skills/production-engineering-loop/references/codex-review.md) includes a personal/project reviewer configuration example; it does not change global settings automatically.

See the [implementation and evaluation record](docs/engineering-loop/features/automated-review-resolution.md) for current results and remaining coverage. Plugin/hook packaging and hosted CI review remain optional future adapters.

## A project memory that grows with the code

On first substantive use, the agent reads the problem statement, maps the existing codebase, and reuses your documentation or creates:

```text
docs/engineering-loop/
  PROJECT.md                   Product intent, stack, architecture, file map
  features/<feature-slug>.md    Criteria, evaluations, changed files, results
  LESSONS.md                   Created only for an evidenced reusable lesson
```

For a new project, stack decisions and files start as proposals and plans. For an existing project, the map records what was actually inspected, including unread areas. A whole-codebase request is handled in batches with a coverage ledger; ordinary tasks focus on the relevant subsystem.

For each meaningful feature change, the agent defines expected behavior and failure cases before implementation, builds or extends appropriate checks, then records actual results. A missed edge case becomes a regression check and, when useful, a lesson with evidence and applicability. Later tasks load the relevant records and verify them against current code. Created, changed, renamed, and removed files are recorded without attributing unrelated edits to the task.

“Self-improving” means improving project knowledge and evaluations through observed outcomes. It does not retrain the model, run in the background, automatically build the backlog, or rewrite the installed skill. Review-only tasks propose memory updates without writing files. Narrow instructions such as “edit only this file” still take precedence.

Try:

```text
Use $production-engineering-loop to read this problem statement and inspect
the existing codebase. Document the product, stack, file responsibilities,
and inspection gaps. Define evaluations for the requested feature, then
implement it and update the project records with actual results.
```

See this repository's own [project context](docs/engineering-loop/PROJECT.md) and [learning-loop feature record](docs/engineering-loop/features/project-learning.md) for a filled example. Those records describe this skill repository, not a fictional application.

For the detailed execution flow, memory lifecycle, optional automation components, and how to prove learning across fresh sessions, read the [self-learning implementation design](docs/self-learning-implementation.md). It distinguishes the existing workflow from proposed automation.

## Feature contracts that reduce repeated discovery

The [full feature template](skills/production-engineering-loop/assets/feature-template.md) preserves the maintainer's PRI-style problem, goal, change contract, risk assessment, implementation plan, security/privacy, acceptance, verification, rollout, progress, decisions, and final pre-merge evidence sections, with explicit design and quality constraints. The [compact template](skills/production-engineering-loop/assets/feature-compact-template.md) retains the essential contract, design, checks, and handoff for bounded work. Use a verified issue identifier or an explicitly unassigned title.

Its added **Execution Context** provides a compact starting point: the next incomplete step, repository-relative paths and symbols, edit/read/test/config roles, relevant callers, check commands, and the source snapshot supporting the map. Locations are marked verified, candidate, or planned. An extra handoff section records relevant learning and refreshed context.

The agent reads the active contract and mapped source, follows scoped searches, and widens inspection when stale paths, changed dependencies, or failures require it. Keep requirements intact; reduce repeated discovery and unrelated code loading. Initial mapping has a cost, and no token-saving percentage has been measured. See the [retrieval workflow](skills/production-engineering-loop/references/task-context.md) and this repository's [feature-contract example](docs/engineering-loop/features/feature-context.md).

When executable testing is meaningful, the supplied plan follows red/green: add the regression case, confirm the intended failure, implement, then refactor with passing tests. Missing tooling is a blocker. A justified TDD exception names structural or repository-native evidence when executable testing is not meaningful.

## Compatibility and validation

Native skill paths are documented for Codex, Claude Code, Cursor, GitHub Copilot, and Gemini CLI. This is documentation-based compatibility, not a claim that every model or product version has been tested. Tools without native skills can use explicit file-based instructions if they can read the package. See [the compatibility guide](docs/installation.md).

Initial v0.1.0 validation on 2026-09-17 passed: skill format checks, eight packaging-validator tests, and a disposable project installation using Skills CLI 1.7.0 targeting all five listed agents. The installer produced shared `.agents/skills` and `.claude/skills` copies; every installed package file matched the source. Validation evidence for the v0.2.0 learning loop is maintained in its [feature record](docs/engineering-loop/features/project-learning.md).

The v0.3.0 feature-contract and focused-retrieval changes have their own [evidence record](docs/engineering-loop/features/feature-context.md). A [subsequent audit](docs/audit-2026-09-18.md) records that snapshot's bounded continuation and no-skill comparison. v0.4.0 made quality primary and added compact/full documentation; see its [feature record](docs/engineering-loop/features/quality-first-modes.md). v0.5.0 adds fresh review orchestration, execution-boundary guidance, findings resolution, and optional provenance helpers. Earlier results are historical, not proof of revised behavior.

These checks do **not** demonstrate engineering quality, host activation, or instruction following. Use the [behavioral evaluation scenarios](evals/README.md) to evaluate actual runs and record the agent, model, version, and outcomes. No cross-agent behavioral benchmark has been established for this initial version.

## Develop and publish

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s tests -v
```

On Windows, use `.venv\Scripts\python.exe` instead of `.venv/bin/python`. GitHub Actions runs the same package checks and validator tests. See [CONTRIBUTING.md](CONTRIBUTING.md) for changes and [the publication checklist](docs/publishing.md) for the initial release.

## License and origin

[MIT](LICENSE). Adapted from the maintainer's personal `engineering-loop` workflow. The public skill uses the name `production-engineering-loop`; avoid enabling both versions for the same task if their guidance overlaps.
