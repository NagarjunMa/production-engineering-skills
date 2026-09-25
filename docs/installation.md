# Installation and compatibility

Production Engineering Loop uses the open Agent Skills `SKILL.md` format. The same package is intended for Codex, Claude Code, Cursor, Gemini CLI, Qwen Code, OpenCode, and other compatible agents. Host-specific files are optional adapters: `agents/openai.yaml` improves Codex presentation, and `references/codex-review.md` plus `assets/pel-reviewer.toml` describe optional Codex review orchestration. Other hosts can ignore those files without losing the core Understand → Build → Verify → Learn workflow.

Install the folder `skills/production-engineering-loop`, not an isolated `SKILL.md`. Keep `references/`, `assets/`, `scripts/`, `agents/`, and `LICENSE` beside it so relative resources remain available. Root-level tests, evaluations, media, and development documentation are publication evidence rather than runtime dependencies.

## Fastest installation

The interactive command discovers the package and, in a normal terminal, asks which coding agents and scope to target:

```sh
npx skills add NagarjunMa/production-engineering-skills
```

The prompt flow is:

1. Select one or more agents.
2. Choose **Project** for the current repository or **Global** for use across local projects.
3. Review the destination summary and confirm.

An agent-integrated terminal can detect the active host and install for it without showing the agent picker. Use an explicit `-a` command when a different target is required. Scope controls the destination, while every selected destination receives the same complete skill directory. The installer does not include this repository's tests, evaluations, documentation, or media in the installed skill.

For one personal/global installation, choose the relevant identifier:

```sh
# Codex
npx skills add NagarjunMa/production-engineering-skills -g -a codex -y

# Claude Code
npx skills add NagarjunMa/production-engineering-skills -g -a claude-code -y

# Cursor
npx skills add NagarjunMa/production-engineering-skills -g -a cursor -y

# Gemini CLI
npx skills add NagarjunMa/production-engineering-skills -g -a gemini-cli -y

# Qwen Code
npx skills add NagarjunMa/production-engineering-skills -g -a qwen-code -y

# OpenCode
npx skills add NagarjunMa/production-engineering-skills -g -a opencode -y
```

One command can target every documented host:

```sh
npx skills add NagarjunMa/production-engineering-skills -g \
  -a codex -a claude-code -a cursor -a gemini-cli -a qwen-code -a opencode -y
```

Omit `-g` for project installation. Install only for agents you actually use. Avoid duplicate personal and project copies unless different versions are intentional.

The GitHub/Skills CLI route requires Node.js 22.20 or newer, npm, and Git. Manual installation and the core workflow require none of them. The optional source-evidence helper requires Python 3.10+ and Git.

## Native skill locations

Vendor and Skills CLI documentation checked on 2026-09-23. Each path is the parent into which the complete `production-engineering-loop` folder is installed.

| Tool | Skills CLI ID | Project directory | Personal directory | Documentation |
| --- | --- | --- | --- | --- |
| Codex | `codex` | `.agents/skills/` | `~/.codex/skills/` | [OpenAI](https://developers.openai.com/codex/skills) |
| Claude Code | `claude-code` | `.claude/skills/` | `~/.claude/skills/` | [Anthropic](https://code.claude.com/docs/en/skills) |
| Cursor | `cursor` | `.agents/skills/` or `.cursor/skills/` | `~/.cursor/skills/` | [Cursor](https://cursor.com/docs/skills) |
| Gemini CLI | `gemini-cli` | `.agents/skills/` or `.gemini/skills/` | `~/.gemini/skills/` | [Gemini CLI](https://geminicli.com/docs/cli/using-agent-skills/) |
| Qwen Code | `qwen-code` | `.qwen/skills/` | `~/.qwen/skills/` | [Qwen Code](https://qwenlm.github.io/qwen-code-docs/en/users/features/skills/) |
| OpenCode | `opencode` | `.agents/skills/` or `.opencode/skills/` | `~/.config/opencode/skills/` | [OpenCode](https://opencode.ai/docs/skills/) |

Personal directories on a laptop are not automatically available to cloud agents. Use the host's documented sync feature or commit a project installation when the remote environment must load the skill. Project installation changes the repository, so follow the team's contribution policy.

## Invoke and verify discovery

| Host | Explicit use | Discovery check |
| --- | --- | --- |
| Codex | `$production-engineering-loop` | Confirm it appears once in the skill list. |
| Claude Code | `/production-engineering-loop` | Type `/` and find `production-engineering-loop`. |
| Cursor | `/production-engineering-loop` or attach with `@` | Open Customize → Skills or search the `/` menu. |
| Gemini CLI | Ask it to use `production-engineering-loop` | Run `/skills list`; use `/skills reload` after changes. |
| Qwen Code | `/production-engineering-loop` | Run `/skills` or use slash-command autocomplete. |
| OpenCode | Ask it to use `production-engineering-loop` | Run `opencode debug skill`. |

Start with a bounded, read-only request so discovery and instruction following are visible without changing source:

```text
Use the production-engineering-loop skill to review the current uncommitted changes.
Do not edit files. Check behavior, affected callers, modularity, duplication,
and relevant tests. Report exact evidence and remaining limitations.
```

Discovery proves only that the host loaded the package. It does not prove that every host model will follow the workflow equally well. Validate behavior on a known task and record the host/version, source state, checks, findings, and limitations.

## Manual project installation

Run from the target project's root. This example uses the shared `.agents/skills` location recognized by Codex, Cursor, Gemini CLI, and OpenCode. Use `.claude/skills` for Claude Code or `.qwen/skills` for Qwen Code. The example refuses to overwrite an existing installation.

macOS/Linux:

```sh
skill_source="/absolute/path/to/production-engineering-loop/skills/production-engineering-loop"
skill_dest=".agents/skills/production-engineering-loop"
if [ -e "$skill_dest" ] || [ -L "$skill_dest" ]; then
  printf 'Installation exists: %s\n' "$skill_dest"
else
  mkdir -p .agents/skills && cp -R "$skill_source" "$skill_dest"
fi
```

Windows PowerShell:

```powershell
$skillSource = 'C:\path\to\production-engineering-loop\skills\production-engineering-loop'
$skillDest = '.agents\skills\production-engineering-loop'
if (Test-Path $skillDest) {
    throw "Installation already exists: $skillDest"
}
New-Item -ItemType Directory -Force '.agents\skills' | Out-Null
Copy-Item -Recurse $skillSource $skillDest
```

Reload the host's skills or start a new session. For updates, compare local modifications before replacing the folder. For removal, delete only the installed `production-engineering-loop` folder or use `npx skills remove` with the same scope and agent identifier used during installation.

## Capability differences

The engineering contract is the same on every host, while orchestration differs:

- File, search, edit, shell, browser, planning, and approval tool names vary. The skill asks the active agent to use its available safe equivalents.
- Codex UI metadata is ignored by other hosts. It does not contain core workflow instructions.
- Fresh reviewer delegation is optional. Hosts with subagents or isolated contexts can automate it; other hosts produce the same portable review packet for a separate session, model, human, or CI job.
- If a host cannot execute commands, it can still inspect source and design, but it must mark executable verification as not run.
- If Python or Git is unavailable, the core workflow remains usable and evidence is recorded manually instead of through the optional helper.
- Permissions remain controlled by the host and user. Installing a skill does not grant filesystem, shell, network, production, or external-service access.

## Other tools and instruction-file fallback

If an agent can read repository files but lacks native Agent Skills discovery, copy the complete package into `docs/skills/production-engineering-loop/` and use:

```text
Read docs/skills/production-engineering-loop/SKILL.md and apply it to this task.
Resolve its relative references within that skill folder.
Task: [describe the outcome and constraints].
```

For repeated use, add a short routing instruction to the repository instruction file the host actually supports while preserving existing content. No filename such as `AGENTS.md` is universal. If the agent cannot read files, provide `SKILL.md` and only the relevant referenced material as prompt context.

This fallback reuses the workflow; it is not native installation support or a guarantee of equivalent behavior. No installer can add capabilities a host does not expose.
