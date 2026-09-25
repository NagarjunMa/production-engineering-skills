# Production Engineering Loop

**Build maintainable code. Verify its behavior. Carry that discipline between projects.**

[![Validate skill package](https://github.com/NagarjunMa/production-engineering-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/NagarjunMa/production-engineering-skills/actions/workflows/validate.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skill metadata](https://img.shields.io/badge/skill-v0.6.0-4c1.svg)](skills/production-engineering-loop/SKILL.md)

A portable skill for AI coding agents that turns implementation into a bounded loop:

```text
Read problem + project memory → Inspect source → Define feature evaluations
         ↑                                                 ↓
Update project map + lessons ← Verify ← Review ← Implement / fix
                               Stop when the contract is met.
```

Use it to build features, fix bugs, review changes, and refactor existing code. It starts from the problem statement and the relevant source, retains verified project knowledge across tasks, scales scrutiny to risk, and requires evidence before claiming success. It works with new or existing projects, with or without a formal implementation plan, commit, branch, or GitHub repository.

The same package is designed for **Codex, Claude Code, Cursor, Gemini CLI, Qwen Code, and OpenCode**. Its core workflow uses the open Agent Skills format and does not depend on one vendor's tool names, subagent system, or UI metadata.

**Start here:** [Quick start](#quick-start) · [Daily workflow](#how-it-changes-the-daily-development-workflow) · [Reliability](#what-can-you-rely-on) · [Installation](#install-for-a-new-user) · [Examples](#use-it-on-real-work) · [Troubleshooting](#troubleshooting)

## Quick start

For a project installation, use Node.js 22.20 or newer, npm, and Git. Open a terminal in that project's root and install the skill:

```sh
cd /path/to/your-project
npx skills add NagarjunMa/production-engineering-skills
```

Choose your coding agent when the installer asks. Open that agent in the project and give it a real outcome:

```text
Use the production-engineering-loop skill to implement this task.
First inspect the relevant code and existing project conventions. Define the
acceptance and failure cases, make the smallest coherent change, run the relevant
checks, review the result, and report anything that remains unverified.

Task: [describe the behavior you want and any constraints]
```

The expected result is more than a code diff. The agent should explain the behavior and constraints the change must satisfy (its change contract), the affected boundaries it inspected, the checks it actually ran, the findings it resolved, and any remaining risk. Start with [installation](#install-for-a-new-user) if you want the skill available across every project or need a specific agent or manual path.

## Who is it for?

| User | How it helps |
| --- | --- |
| Software engineer | Adds repeatable contract, architecture, regression, compatibility, and review discipline around agent-generated changes. |
| Tech lead or maintainer | Keeps shared rules, affected consumers, rollout risk, and verification evidence visible across contributors and sessions. |
| Solo builder | Supplies a practical definition of done without requiring enterprise infrastructure or a large process. |
| Builder without a traditional engineering background | Turns a desired outcome into acceptance cases, repository-aware implementation, tests, review, and an honest handoff. |
| Reviewer | Supports read-only inspection or evidence-backed review-and-fix against committed, staged, or uncommitted source. |

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

## How it changes the daily development workflow

The skill does not replace normal engineering work. It makes the important parts explicit and asks the agent to carry them through to completion. Skip it for copy-only edits, simple explanations, and status reports where no engineering decision or source evaluation is needed.

| Daily moment | Without a defined loop | With Production Engineering Loop |
| --- | --- | --- |
| Starting a task | The agent may begin editing from the prompt alone | It reads the request, relevant source, repository instructions, tests, and existing project records before selecting an approach |
| Planning | Success can remain subjective | The agent defines observable acceptance cases, failure paths, scope, invariants, and risk |
| Coding | A plausible local solution may ignore callers or duplicate rules | The agent checks affected consumers, canonical business rules, existing patterns, and responsibility boundaries |
| Testing | “Tests pass” may mean one convenient command | The agent maps criteria to checks and distinguishes passed, failed, blocked, skipped, and not-run evidence |
| Reviewing | Suggestions may be implemented without validation | Findings are verified against the contract and source, classified, resolved with evidence, or dismissed with a reason |
| Handoff | The next session has to rediscover the work | The project map and feature record retain current paths, decisions, actual results, remaining work, and proven lessons |

For a bounded everyday change, use compact mode and let the agent keep the record short. For public contracts, migrations, authentication, payments, shared architecture, or other high-impact work, the skill expands the design, compatibility, security, rollback, and review evidence.

The first substantive run can take longer because the agent must learn the relevant part of the repository. Later runs can reuse verified project context, but the skill refreshes stale paths and never treats saved documentation as more authoritative than the current source.

## How it supports development standards

“Industry standard” is not one universal checklist. The skill first follows the repository's established sound conventions and required checks. Where the project has no clear convention, it asks for the smallest design that makes ownership, dependencies, behavior, and failure handling explicit.

| Quality area | Practice applied | Evidence expected before completion |
| --- | --- | --- |
| Requirements | Observable behavior, non-goals, invariants, and material failure cases | Acceptance criteria mapped to implementation and checks |
| Architecture | Existing pattern fit, cohesive responsibilities, dependency direction, and justified abstractions | Relevant callers and boundaries inspected; design choice recorded when material |
| Correctness | Success, edge, negative, state-transition, and recovery behavior | Meaningful behavioral or regression checks with actual results |
| Maintainability | One appropriate owner for shared rules, intentional differences preserved, dead or redundant code avoided | Diff and affected-path review, with duplication decisions explained when material |
| Security and privacy | Authorization, validation, secrets, sensitive logging, data handling, abuse paths, and trust boundaries considered when relevant | Adversarial cases or explicit limitations proportional to risk |
| Compatibility | APIs, schemas, stored data, clients, configuration, defaults, and independently deployed consumers considered | Compatibility evidence plus migration or rollback plan when needed |
| Verification integrity | No fabricated results, hidden failures, weakened tests, or stale review evidence | Exact commands/procedures, tested source state, and unresolved blockers reported |
| Delivery | Implemented, verified, released, and deployed remain distinct states | Honest handoff with remaining risks and required next action |

This process can help a project reach a higher standard, but it cannot supply missing product decisions, domain expertise, realistic test environments, or human release authority. Repository policies and qualified review remain decisive.

## What can you rely on?

Reliability has four different layers:

| Layer | What is established |
| --- | --- |
| Package | The installable folder is self-contained, uses the Agent Skills format, has no installation hook or required API key, and passed package/link validation. |
| Deterministic helper | The optional evidence helper has executable regression coverage, forces Git inventory operations offline, detects stale source packets, and validates report structure. It does not judge code quality or prove that a reported check ran. |
| Agent behavior | The instructions define scope, review, verification, and stopping rules, but the host model and available tools determine how faithfully and effectively they are applied. |
| Project outcome | Confidence comes from the acceptance cases, source inspection, tests, review, and limitations produced for that specific task. Installing the skill alone is not evidence that a change is correct. |

Current local v0.6 evidence includes 29 tests, package and skill-format validation, a byte-for-byte Skills CLI installation targeting all six documented hosts, and native OpenCode discovery. The last public v0.5 revision additionally has Codex discovery, dependency auditing, and a five-job GitHub Actions matrix across Ubuntu, macOS, Windows, and Python 3.10–3.12. The security correction for the optional Git helper was independently reproduced with a positive control and return review. See the [current publication audit](docs/publication-audit-2026-09-20.md) and [retained evaluation evidence](evals/README.md) for scope and limitations.

The evaluations do **not** prove a universal improvement over a capable baseline, a defect-free result, reliable activation in every coding tool, or measured quality-per-token gains. Evaluate the skill on representative work in your own repository before making it a required team workflow.

## If you are new to software development

You do not need to know every design pattern or test framework to use the skill. Give the agent the behavior you want, the users affected, examples of correct and incorrect outcomes, and constraints you already know. Let it inspect the repository before it proposes architecture.

Use these guardrails:

1. Start with a small task or a review-only run so you can inspect the workflow without risking a large change.
2. Ask for compact mode unless the change affects authentication, payments, stored data, migrations, public APIs, permissions, or other high-impact boundaries.
3. Read the final **failed**, **blocked**, and **not run** checks. Generated code is not finished merely because some tests passed.
4. Do not authorize deployment, destructive data changes, credential changes, or production access solely because the agent reports success.
5. Ask a qualified engineer or domain reviewer to inspect security-sensitive, financial, legal, privacy, migration, and production-critical work.

A useful first request is:

```text
Use $production-engineering-loop in review-only mode. Explain the current change
in plain language, identify the behavior it is supposed to preserve, run safe
relevant checks, and list material problems or missing evidence. Do not edit files.
```

## What it does not promise

This skill does not guarantee perfect or vulnerability-free code, certify compliance, replace required human review, make deployment decisions, or prove that a reported test actually ran. Model capability, repository context, available tools, permissions, tests, and reviewer judgment still determine the outcome.

It does not retrain the model or silently modify itself. Its “self-improving” loop improves repository knowledge, feature evaluations, and regression evidence after observed outcomes. It does not run in the background or automatically create a backlog.

## Install for a new user

The complete installable package is the [skills/production-engineering-loop](skills/production-engineering-loop/SKILL.md) folder. It contains the portable skill entrypoint, supporting references, templates, optional evidence helper, host compatibility guidance, optional Codex UI/reviewer metadata, and the license. The Codex files are adapters; other hosts ignore them and use the same core workflow. Repository-level tests, evaluation artifacts, and development documentation are not runtime dependencies.

The package uses the open [Agent Skills format](https://agentskills.io/specification). Normal use requires no API key, MCP server, background service, installation hook, Python runtime, or GitHub account. The documented GitHub installation requires Node.js 22.20 or newer, npm, and Git. Manual installation and the core workflow require none of those tools. The optional source-evidence helper requires Git and Python 3.10+.

### 1. Choose the installation scope

| Scope | Choose it when | Result |
| --- | --- | --- |
| Personal/global | You want the skill available in all of your local projects | Installed in the coding tool's personal skills directory |
| Project | A team or one repository should use and version the skill | Installed under the current project's supported skills directory |

Avoid installing both personal and project copies unless you intentionally need different versions. Multiple discoverable copies can make it unclear which instructions the agent loaded.

### 2. Install from GitHub

The repository contains one installable skill, so the shortest command is:

```sh
npx skills add NagarjunMa/production-engineering-skills
```

In a normal terminal, the installer presents this flow:

1. Select one or more coding agents from the detected/supported agent list.
2. Choose **Project** to install in the current repository or **Global** to make the skill available across your local projects.
3. Review the destination summary and confirm the installation.

An agent-integrated terminal may detect the active coding agent and skip the agent picker. Use one of the explicit commands below when you want a different target or a fully repeatable installation.

The selected agent and scope determine **where** the skill is installed. Every destination receives the same complete, self-contained `production-engineering-loop` package so its shared references, templates, helper, and license remain available. Repository development files such as tests, evaluations, documentation, and media are not installed with the skill.

If you prefer a direct command, choose **one tool below**. Use the personal command to make the skill available across your projects, or run the project command from a repository root to install it only there.

#### Codex

Personal installation:

```sh
npx skills add NagarjunMa/production-engineering-skills -g -a codex -y
```

Project installation:

```sh
npx skills add NagarjunMa/production-engineering-skills -a codex -y
```

Invoke with `$production-engineering-loop`.

#### Claude Code

Personal installation:

```sh
npx skills add NagarjunMa/production-engineering-skills -g -a claude-code -y
```

Project installation:

```sh
npx skills add NagarjunMa/production-engineering-skills -a claude-code -y
```

Invoke with `/production-engineering-loop`.

#### Cursor

Personal installation:

```sh
npx skills add NagarjunMa/production-engineering-skills -g -a cursor -y
```

Project installation:

```sh
npx skills add NagarjunMa/production-engineering-skills -a cursor -y
```

Invoke with `/production-engineering-loop` or attach it with `@`.

#### Gemini CLI

Personal installation:

```sh
npx skills add NagarjunMa/production-engineering-skills -g -a gemini-cli -y
```

Project installation:

```sh
npx skills add NagarjunMa/production-engineering-skills -a gemini-cli -y
```

Confirm discovery with `/skills list`, then ask Gemini to use `production-engineering-loop`.

#### Qwen Code

Personal installation:

```sh
npx skills add NagarjunMa/production-engineering-skills -g -a qwen-code -y
```

Project installation:

```sh
npx skills add NagarjunMa/production-engineering-skills -a qwen-code -y
```

Invoke with `/production-engineering-loop`.

#### OpenCode

Personal installation:

```sh
npx skills add NagarjunMa/production-engineering-skills -g -a opencode -y
```

Project installation:

```sh
npx skills add NagarjunMa/production-engineering-skills -a opencode -y
```

Ask OpenCode to use `production-engineering-loop`. Confirm discovery with `opencode debug skill`.

Install only for tools you use. Avoid installing both personal and project copies for the same tool unless you intentionally maintain different versions. The [Skills CLI](https://github.com/vercel-labs/skills) supports additional agents beyond the six documented here.

### 3. Install from a local clone

To test or develop the skill before publication, replace `<agent-id>` with one identifier shown above—for example, `codex`, `claude-code`, or `opencode`:

```sh
npx skills add /absolute/path/to/production-engineering-loop \
  --skill production-engineering-loop --agent <agent-id> --yes
```

Add `--global` when you want that local installation available across projects.

### 4. Install manually when needed

Copy the **whole** `skills/production-engineering-loop` directory into the host's personal or project skills directory. Do not copy only `SKILL.md`; its references, templates, license, helper, and metadata are part of the package.

| Coding agent | Project parent | Personal parent |
| --- | --- | --- |
| Codex | `.agents/skills/` | `~/.codex/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.agents/skills/` or `.cursor/skills/` | `~/.cursor/skills/` |
| Gemini CLI | `.agents/skills/` or `.gemini/skills/` | `~/.gemini/skills/` |
| Qwen Code | `.qwen/skills/` | `~/.qwen/skills/` |
| OpenCode | `.agents/skills/` or `.opencode/skills/` | `~/.config/opencode/skills/` |

The [installation and compatibility guide](docs/installation.md) contains host-specific discovery checks, Windows instructions, update/removal guidance, and a file-based fallback for tools without native skill support.

### 5. Confirm the installation

1. Restart or reload the coding tool if it does not refresh skills automatically.
2. Open the tool's skill list and confirm that **Production Engineering Loop** appears once and is enabled.
3. Use the invocation shown under your coding tool above, followed by an explicit, bounded request.

Use this host-neutral first task:

```text
Use the production-engineering-loop skill to review the current uncommitted changes.
Do not edit files. Check behavior, affected callers, modularity, duplication,
and the relevant tests. Report exact evidence and remaining limitations.
```

Installation proves that the host can discover the package. It does not by itself prove that every model will follow every instruction correctly. Evaluate a known task and inspect the resulting plan, changes, checks, and review evidence.

### 6. Update or remove it

Update a personal installation:

```sh
npx skills update production-engineering-loop -g -y
```

Update the current project's installation:

```sh
npx skills update production-engineering-loop -p -y
```

Remove a personal installation from one or more hosts by naming their agent identifiers:

```sh
npx skills remove production-engineering-loop -g -a claude-code -a opencode -y
```

Removing the installed skill does not remove project documentation the agent previously created. Those records belong to the project and should be reviewed like any other repository files.

## Security and permissions

Installing the skill adds instructions and bundled resources. It does not install a background service, request an API key, connect an external account, add an MCP server, or run code automatically. The optional Python helper runs only when the agent invokes that review-evidence workflow.

The coding agent still has the permissions supplied by its host and by you. A skill is guidance, not a sandbox. Review commands before granting elevated access, keep credentials out of prompts and repositories, and retain your normal approval controls for deployments, production data, destructive operations, and external communications.

Review-only mode instructs the agent not to edit source or mutate external systems. When the host supports read-only controls or isolated scratch environments, the skill asks the agent to use them. The optional Git evidence helper disables transports and lazy fetching so missing objects fail instead of causing a network fetch or remote-helper execution.

See [SECURITY.md](SECURITY.md) for the supported-version and vulnerability-reporting policy.

## Troubleshooting

| Symptom | What to do |
| --- | --- |
| Skill does not appear | Restart or reload the agent, then run `npx skills list` or `npx skills ls -g`. Confirm the package was installed for the intended agent and scope. |
| Skill appears twice | Remove either the personal or project copy, then reload. Keep both only when you intentionally manage different versions. |
| Agent does not activate it automatically | Use the host-specific invocation in the installation table, or ask the agent to read the installed `SKILL.md` and apply it to the task. |
| Agent produces too much documentation | Request compact mode. The engineering checks stay applicable while the written record becomes shorter. |
| Fresh review cannot run | The agent should prepare the portable review packet and mark independent review pending; it must not claim that self-review satisfied the requirement. |
| Project has no tests | For executable behavior, the agent should add the smallest meaningful test setup when authorized and practical. Missing tooling or prerequisites are blockers, not permission to substitute prose. Structural/manual verification is appropriate only when executable testing is not meaningful, and the limitation must be explicit. |
| Python is unavailable | Continue with the core workflow and manual evidence. Only the optional provenance helper requires Python 3.10+. |
| Git is unavailable | Install the package manually and use the core workflow without the provenance helper. The documented GitHub CLI installation and optional helper require Git. |
| First task feels slow | Start with a bounded subsystem. Initial repository mapping costs time; later tasks can reuse verified context and refresh only affected areas. |

For host-specific paths, Windows installation, and file-based fallback instructions, use the [installation and compatibility guide](docs/installation.md).

## Use it on real work

Explicitly name the skill and describe the outcome and constraints. You can supply a short task, an issue, or the full feature template bundled with this project.

Implementation example:

```text
Use the production-engineering-loop skill to implement cursor pagination for GET /orders.
Preserve the existing response fields and authorization behavior.
Define the acceptance and failure cases, implement the change, run the relevant
repository checks, review the result, and resolve confirmed findings.
```

Project onboarding and implementation example:

```text
Use the production-engineering-loop skill to read this problem statement and inspect the
relevant codebase. Record the product, stack, architecture, file responsibilities,
and inspection gaps. Define evaluations for the requested feature, implement it,
and update the project records with actual results.
```

Review-and-fix example:

```text
Use the production-engineering-loop skill to review the current branch against this problem
statement. Verify each finding against the current source, fix confirmed in-scope
issues, add regression coverage where appropriate, and rerun affected checks.
```

In Codex, invoke `$production-engineering-loop`. Claude Code, Cursor, and Qwen Code support `/production-engineering-loop`; Cursor also supports attaching the skill with `@`. Gemini CLI and OpenCode can discover it from their skill directories and load it from a direct request. Automatic invocation depends on the host and model, so use the explicit route for the first test.

A useful handoff might look like this **illustrative example**, not a result from this repository:

> Implemented the pagination fix while preserving the response shape. Significant risk: public API contract. Passed: focused pagination tests and type checks. Integration tests were blocked by an unavailable local database. Implementation is complete; integration verification remains pending.

## Evaluate it in your own workflow

Adopt the skill based on observed results in your repositories, not the size or confidence of its output.

1. Choose a bounded task with clear acceptance behavior and at least one meaningful failure path.
2. Preserve the starting source and requirements. If comparing workflows, use equivalent starting states and the same independent acceptance checks.
3. Run the skill explicitly and retain the changed files, commands, results, findings, and limitations.
4. Independently evaluate correctness, compatibility, modularity, duplication, abstraction choices, verification integrity, and whether the documentation matches the code.
5. Record defects caught, defects missed, unsupported suggestions, regressions, elapsed time, and token/tool measurements only when the host exposes them.
6. Repeat on different task types before making the skill mandatory for a team.

A good result is a change whose behavior and affected boundaries are understandable, whose important failure cases are checked, whose design fits the repository, and whose remaining uncertainty is visible. More files, tests, prose, abstractions, or reviewer rounds do not automatically mean higher quality.

Use the [community validation record](docs/community-validation.md) to capture comparable runs without publishing private source, customer data, credentials, or personal paths.

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

The [full feature template](skills/production-engineering-loop/assets/feature-template.md) preserves the maintainer's detailed structure for the problem, goal, change contract, risk assessment, implementation plan, security/privacy, acceptance, verification, rollout, progress, decisions, and final pre-merge evidence, with explicit design and quality constraints. The [compact template](skills/production-engineering-loop/assets/feature-compact-template.md) retains the essential contract, design, checks, and handoff for bounded work. Use a verified issue identifier or an explicitly unassigned title.

Its added **Execution Context** provides a compact starting point: the next incomplete step, repository-relative paths and symbols, edit/read/test/config roles, relevant callers, check commands, and the source snapshot supporting the map. Locations are marked verified, candidate, or planned. An extra handoff section records relevant learning and refreshed context.

The agent reads the active contract and mapped source, follows scoped searches, and widens inspection when stale paths, changed dependencies, or failures require it. Keep requirements intact; reduce repeated discovery and unrelated code loading. Initial mapping has a cost, and no token-saving percentage has been measured. See the [retrieval workflow](skills/production-engineering-loop/references/task-context.md) and this repository's [feature-contract example](docs/engineering-loop/features/feature-context.md).

When executable testing is meaningful, the supplied plan follows red/green: add the regression case, confirm the intended failure, implement, then refactor with passing tests. Missing tooling is a blocker. A justified TDD exception names structural or repository-native evidence when executable testing is not meaningful.

## Compatibility and validation

| Environment | Current evidence |
| --- | --- |
| Codex desktop/CLI on macOS | Public and local installation, personal/project discovery, nested-project discovery, explicit invocation, and fresh-review workflow exercised |
| GitHub Actions | [Run 35556792913](https://github.com/NagarjunMa/production-engineering-skills/actions/runs/35556792913) passed all five package-validation and test jobs for public `main` commit `a588182` across Ubuntu Python 3.10–3.12, macOS Python 3.11, and Windows Python 3.11 |
| Skills CLI | The public repository exposes one skill; local multi-target installation verifies the same package layout for Codex, Claude Code, Cursor, Gemini CLI, Qwen Code, and OpenCode |
| Claude Code and OpenCode installed locally | The multi-target installer produced both host layouts and OpenCode discovered the exact current package; Claude Code runtime discovery and full task-behavior evaluations remain pending |
| Cursor, Gemini CLI, and Qwen Code | Native paths and invocation are documented from current vendor guidance; full task behavior has not yet been independently exercised on these hosts |
| Other file-capable agents | Can use the bundled `SKILL.md` and relative resources explicitly; this is a fallback rather than verified native integration |

The repository retains source snapshots, deterministic checks, behavioral scenarios, independent findings, corrections, and limitations. Historical v0.1–v0.5 records explain how the current v0.6 workflow developed; they are not treated as proof of current behavior. Start with the [publication audit](docs/publication-audit-2026-09-20.md), [evaluation index](evals/README.md), and [community validation template](docs/community-validation.md).

Native skill paths are documented for Codex, Claude Code, Cursor, Gemini CLI, Qwen Code, and OpenCode in the [compatibility guide](docs/installation.md). Product versions, organizational policies, available models, and tool permissions can change actual behavior.

## Support and feedback

Report reproducible bugs, documentation gaps, and compatibility results in [GitHub Issues](https://github.com/NagarjunMa/production-engineering-skills/issues). Include the host tool and version, installation scope, skill version or source revision, task type, observed behavior, and a minimal sanitized reproduction when possible. Never publish credentials, customer data, private source, or personal paths.

For suspected security vulnerabilities, follow [SECURITY.md](SECURITY.md) instead of opening a public issue. Use the [community validation record](docs/community-validation.md) when sharing evidence from a real project.

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
