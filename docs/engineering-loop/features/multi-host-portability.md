# Unassigned — Multi-host Agent Skills portability

## Contract and context

- Requirement source and intended outcome: Make Production Engineering Loop a first-class skill for Codex and Claude Code while supporting Cursor, Gemini CLI, Qwen Code, and OpenCode from the same package.
- Included scope: host-neutral core language, standard compatibility metadata, native/CLI installation paths, invocation and discovery checks, capability fallbacks, package validation in each documented directory layout, and honest support claims.
- Non-goals: claiming equal model behavior, bundling six vendor-specific plugins, requiring subagents, or certifying untested cloud/organization configurations.
- Invariants and material failure cases: the core workflow and evidence standards remain unchanged; optional Codex metadata must not become a dependency; every relative resource must survive installation; unsupported host behavior must remain labeled unverified.
- Risk tier and affected boundaries: Standard documentation/package-interface change affecting discovery, installation, and user expectations.
- Documentation mode: Compact — behavior is bounded to package portability and has no application runtime.
- Verified source snapshot and worktree state: local working tree with pre-existing README/publication documentation edits and new uncommitted media; unrelated edits preserved.
- Implementation status: Implemented locally; verification recorded below.

| Path and symbol | Role and relevance | Status |
| --- | --- | --- |
| `skills/production-engineering-loop/SKILL.md` | Portable metadata and host-neutral execution contract | Changed and inspected |
| `skills/production-engineering-loop/references/host-compatibility.md` | Installed six-host compatibility reference | Created and inspected |
| `skills/production-engineering-loop/references/independent-review.md` | Routes fresh review through host capability rather than Codex alone | Changed and inspected |
| `README.md`, `docs/installation.md` | User-facing installation, invocation, support, and evidence boundaries | Changed and inspected |
| `scripts/validate.py`, `tests/test_validate.py` | Standard compatibility validation and copied-layout regressions | Changed; executable checks required |

## Design and quality

- Reuse the Agent Skills standard directory as the canonical package. Do not fork instructions per vendor.
- Keep host-specific behavior in a progressively loaded reference. Retain `agents/openai.yaml` and the Codex reviewer adapter as optional enhancements.
- Use the Skills CLI's documented identifiers for automated installation. Keep manual paths and direct host checks available when the CLI is not used.
- Treat package validation, host discovery, instruction following, and engineering outcomes as separate evidence levels.
- Installation does not grant additional permissions or make local personal skills available to remote/cloud sessions.

## Acceptance and verification

| ID | Observable outcome / forbidden effect | Procedure | Result |
| --- | --- | --- | --- |
| P1 | One complete package validates after copying into all six documented native layouts | Run packaging unit tests | Passed: 29-test suite includes six copied-layout cases |
| P2 | Skills CLI can target Codex, Claude Code, Cursor, Gemini CLI, Qwen Code, and OpenCode from the local repository | Install into a disposable project with all six `-a` identifiers; compare installed package files | Passed: `.agents`, `.claude`, and `.qwen` destinations each matched all 25 source files |
| P3 | OpenCode discovers the installed package without model execution | Run `opencode debug skill` in the disposable project | Passed on OpenCode 1.18.27 with isolated user configuration |
| P4 | Core instructions do not require Codex, GitHub, hosted CI, or subagent support | Inspect `SKILL.md` and host reference; validate local links | Passed: repository validator and Codex skill-format validator passed |
| P5 | Public claims distinguish install/package evidence from real task behavior | Review README compatibility table and installation guide | Passed by source review; non-Codex task behavior remains explicitly pending |
| P6 | The short install command offers agent and Project/Global selection outside an agent-detected session | Run the current Skills CLI in an isolated home and disposable Git repository; stop before installation | Passed on 2026-09-25: agent multi-select and Project/Global scope prompts appeared; a separate Codex-integrated run correctly auto-detected Codex |

## Outcome and handoff

- Actual files: portable compatibility reference added; core metadata/version and independent-review routing updated; README/installation rewritten around six hosts; validator and tests extended.
- Remaining gap: representative end-to-end feature and review tasks have not yet been run in Cursor, Gemini CLI, Qwen Code, or OpenCode. Claude Code/OpenCode local availability does not itself establish model behavior.
- Validation: `scripts/validate.py` passed; skill-creator quick validation passed; 29 tests passed; `git diff --check` passed; disposable six-target installation, interactive agent/scope prompt, agent auto-detection, and OpenCode discovery passed.
- Status: Verified locally. Commit, hosted CI, immutable release, and additional host behavior tests remain separate release steps.
