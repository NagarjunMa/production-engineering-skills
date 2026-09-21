# Codex reviewer adapter

Use when Codex exposes delegation. The portable contract remains in [independent-review.md](independent-review.md).

1. Inspect actual host delegation capabilities. Spawn a fresh context (`fork_turns="none"` when available), passing the contract, source/packet location, and [reviewer prompt](../assets/reviewer-prompt.md). Do not open another user-owned task for this subtask.
2. Use the explicitly selected reviewer model or configured reviewer agent when available. Otherwise inherit the host default and report fresh-context review. Do not guess available models or read credentials/invoke external providers to obtain diversity.
3. If explicitly required cross-model review is unavailable, report that requirement pending. If it was only a preference, disclose the default-model fallback. Do not repeatedly request configuration on every feature.
4. Keep review source read-only. Instructions alone are not a sandbox: use host read-only controls when available, or an isolated copy plus before/after hashes. Report actual isolation. Mutating tests run in authorized scratch space.
5. Wait for the report, verify its evidence/freshness, and perform the parent-owned resolution loop. Supply corrected snapshots, prior finding IDs, and new evidence on return review. Reviewers do not recursively delegate.

Optional setup: when requested, copy [pel-reviewer.toml](../assets/pel-reviewer.toml) into personal `~/.codex/agents/` or project `.codex/agents/`. Preserve existing configuration. The installed skill's `agents/openai.yaml` is UI metadata, not a reviewer role.

The example inherits its model. Set `model` and supported `model_reasoning_effort` after selecting an available model. Dedicated agent configuration scopes the choice; `[agents]` global defaults affect other subagents. Some hosts expose only spawn arguments: use those and report what actually applied, never claim a TOML file was loaded just because it exists.

Official reference checked 2026-09-20: [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents). Host versions/settings differ. This adapter operates during the active task; it installs no background monitor, plugin, hook, or hosted CI job.
