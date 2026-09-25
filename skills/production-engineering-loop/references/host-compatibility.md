# Host compatibility

The core workflow uses the open Agent Skills directory format: a `SKILL.md` entrypoint plus relative `references/`, `assets/`, and optional `scripts/`. Keep the complete directory together. `agents/openai.yaml` improves Codex presentation and is optional metadata; other hosts may ignore it. The Codex reviewer adapter is also optional. Neither is required for understanding, implementation, verification, project learning, or the portable review packet.

## Install and invoke

The Skills CLI can install the same package for each supported host. Its current agent identifiers and native destinations are listed below. Project locations are relative to the target repository.

| Host | Skills CLI ID | Project location | Personal location | Explicit use or discovery check |
| --- | --- | --- | --- | --- |
| Codex | `codex` | `.agents/skills/` | `~/.codex/skills/` | Invoke `$production-engineering-loop` or select it from the skill list. |
| Claude Code | `claude-code` | `.claude/skills/` | `~/.claude/skills/` | Invoke `/production-engineering-loop`. |
| Cursor | `cursor` | `.agents/skills/` or `.cursor/skills/` | `~/.cursor/skills/` | Invoke `/production-engineering-loop` or attach it with `@`. |
| Gemini CLI | `gemini-cli` | `.agents/skills/` or `.gemini/skills/` | `~/.gemini/skills/` | Confirm with `/skills list`, then ask Gemini to use the named skill. |
| Qwen Code | `qwen-code` | `.qwen/skills/` | `~/.qwen/skills/` | Invoke `/production-engineering-loop` or confirm with `/skills`. |
| OpenCode | `opencode` | `.agents/skills/` or `.opencode/skills/` | `~/.config/opencode/skills/` | Ask OpenCode to use the named skill; confirm discovery with `opencode debug skill`. |

Interactive installation is the simplest route because it lets the developer choose the installed coding agents and scope:

```sh
npx skills add NagarjunMa/production-engineering-skills
```

In a normal terminal, select one or more agents, choose Project or Global scope, review the destination summary, and confirm. An agent-integrated terminal may detect the active host and skip the agent picker; use an explicit `-a` option when a different target is required. Agent and scope selection changes the install destination, not the package contents. Install the complete skill directory so every host can resolve the same shared workflow resources.

To install a personal copy for all six hosts in one command:

```sh
npx skills add NagarjunMa/production-engineering-skills -g \
  -a codex -a claude-code -a cursor -a gemini-cli -a qwen-code -a opencode -y
```

To install for one host, retain only its `-a` option. Omit `-g` for a project installation. A manual installation copies the entire `production-engineering-loop` directory into one destination from the table.

## Preserve behavior across hosts

- Resolve linked files relative to the installed skill directory. Do not assume the current working directory contains this package.
- Use the host's native file, search, edit, shell, browser, planning, and approval controls. Tool names differ; the required outcome and evidence do not.
- Respect the host's permission system and the repository's instruction hierarchy. A skill does not grant additional access.
- If automatic activation is unreliable, use the explicit invocation form or ask the agent to read the installed `SKILL.md` and apply it to the task.
- If the host cannot run commands, complete source inspection and structural review, mark executable checks as not run, and report the resulting limitation.
- If the host cannot delegate an independent reviewer, generate the portable review packet and reviewer prompt. Do not relabel a same-context self-review as independent.
- If the optional Python/Git evidence helper is unavailable, record the source state, paths, hashes when available, check results, and freshness limitations manually.

## Capability-specific enhancements

Fresh reviewer orchestration is an enhancement, not part of the portable minimum. When a host offers subagents or isolated contexts, provide only the contract, exact source snapshot, applicable repository instructions, and reviewer prompt. Keep the reviewer read-only and return findings to the coordinating agent for resolution. When it does not, use the same packet with a separate session, model, human reviewer, or CI job.

Host documentation and behavior change over time. Report the product/version, installation scope, discovery result, invocation route, available tools, and any deviations when contributing compatibility evidence.
