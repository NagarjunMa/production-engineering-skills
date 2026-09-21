# Installation and compatibility

Install the folder `skills/production-engineering-loop`, not the repository root. That folder is a complete runtime package: keep `SKILL.md`, `references/`, `assets/`, `scripts/`, `agents/`, and `LICENSE` together. Root-level tests, evaluations, and documentation are development/publication evidence and are not required after installation. The skill has no executable installation hook; its standard-library evidence script runs only when the agent explicitly uses that optional workflow.

## Native skill locations

Vendor documentation checked on 2026-09-17. Each path below is the **parent** into which you copy the `production-engineering-loop` folder. Availability can vary by version, product surface, and organization policy.

| Tool | Project directory | Personal directory | Source |
| --- | --- | --- | --- |
| Codex | `.agents/skills/` | `~/.agents/skills/` | [OpenAI](https://learn.chatgpt.com/docs/build-skills) |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | [Anthropic](https://code.claude.com/docs/en/skills) |
| Cursor | `.cursor/skills/` or `.agents/skills/` | `~/.cursor/skills/` | [Cursor](https://cursor.com/docs/skills) |
| GitHub Copilot | `.github/skills/` or `.agents/skills/` | `~/.copilot/skills/` | [GitHub](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` | `~/.gemini/skills/` | [Gemini CLI](https://geminicli.com/docs/cli/skills/) |

Personal directories on your laptop are not automatically available to remote/cloud agents. Use the host's documented sync mechanism or project installation. Copying a skill into a project is a repository change; follow your team's contribution policy.

GitHub is not required for local use. A developer can install from a local clone or copy the complete folder. Once installed, the workflow can evaluate uncommitted/staged work, a chosen branch or revision range, selected code, or completed existing code. Git and Python 3.10+ are optional requirements of the provenance helper only; the instructions and templates work without them using clearly recorded manual evidence.

The [Skills CLI](https://github.com/vercel-labs/skills) also supports other agents and may choose different supported aliases. Consult its current agent list rather than assuming every agent uses one directory. Do not install duplicate copies in several directories that the same agent scans.

## Manual example: project installation

Run from the target project's root, replacing the source path with your local clone. This example uses `.agents/skills`; substitute the native path from the table if needed. It refuses to overwrite an existing installation.

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

Reload skills or start a new agent session, then confirm the skill appears in the host's skill list. Try an explicit review-only request on a small known diff and inspect whether the agent reads the skill and preserves the worktree. Automatic invocation is a host decision; installation does not ensure activation on every task.

For updates, review the new version and compare any local modifications before replacing the installed folder. For uninstall, remove only the installed `production-engineering-loop` folder or symlink from the chosen scope. If installed with Skills CLI, use its documented `remove` command with the matching scope and agent.

## Other tools and instruction-file fallback

If an agent can read repository files but lacks native skills, copy the package into `docs/skills/production-engineering-loop/` in the target project, then use this prompt:

```text
Read docs/skills/production-engineering-loop/SKILL.md and apply it to this task.
Resolve its relative references within that skill folder.
Task: [describe the outcome and constraints].
```

For repeated use, add that routing instruction to the repository instruction file the host actually supports, preserving its existing content. A filename such as `AGENTS.md` is not universal. If the agent cannot read files, provide the main skill and relevant references as prompt context; automatic discovery and command execution will not be available.

This fallback reuses the workflow; it is not native installation support or a guarantee of equivalent behavior. No universal installer can add capabilities a host does not expose.
