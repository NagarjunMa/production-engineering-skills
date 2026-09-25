# Publication security audit and multi-host portability addendum

**Date:** 2026-09-20; portability addendum 2026-09-23
**Package:** `skills/production-engineering-loop`, local version 0.6.0; public audited revision 0.5.0
**Verdict:** **Local v0.6 release candidate.** The v0.5 security findings remain resolved. The current package validates and installs through the Skills CLI for six host targets, with native OpenCode discovery confirmed. The v0.6 revision still requires commit, hosted CI, immutable release, and release-download verification before those release claims apply to it.

## Current result

The repository was hardened after this audit at the maintainer's request:

- SEC-001: fixed locally. Every helper Git subprocess now forces `GIT_NO_LAZY_FETCH=1`, `GIT_ALLOW_PROTOCOL=''`, `GIT_TERMINAL_PROMPT=0`, and `GIT_OPTIONAL_LOCKS=0`, while retaining filesystem-monitor isolation. A new regression removes a promised base object and verifies that `capture`, `check`, and `validate` all fail without executing the configured remote helper.
- PUB-002: fixed in the candidate public artifacts. The four personal paths were replaced with explicit portable placeholders and marked as sanitized evidence. The installable package continues to contain no personal home paths.
- PUB-003: for public v0.5, the repository is `NagarjunMa/production-engineering-skills`. The short GitHub command found one skill, installed it into a fresh Codex project, and produced a matching package. CI actions are pinned to immutable revisions, Dependabot is configured, and [hosted run 35556792913](https://github.com/NagarjunMa/production-engineering-skills/actions/runs/35556792913) passed all five jobs on public `main` commit `a58818220c8f59fd1717457b73758ef1f0018462`: Ubuntu Python 3.10–3.12, macOS Python 3.11, and Windows Python 3.11. Local v0.6 documentation and metadata are aligned, but a v0.6 hosted run and immutable release installation remain pending.

Local package validation, skill-format validation, dependency audit, and 29 tests pass after the portability changes. A disposable Skills CLI run targeted Codex, Claude Code, Cursor, Gemini CLI, Qwen Code, and OpenCode; its three physical destination copies (`.agents`, `.claude`, and `.qwen`) each matched all 25 current package files. OpenCode 1.18.27 discovered the installed skill from `.agents/skills`. This establishes package/install compatibility, not equal instruction following or engineering outcomes across models. The earlier independent return review reproduced the original hostile setup: an unguarded positive control executed its harmless marker, while the corrected helper's `capture`, `check`, and `validate` commands each failed closed without executing the marker.

The skill can be installed once at personal scope and used across local projects. A project copy also works, including discovery from a nested directory. That does not establish compatibility with every Codex version, organization policy, operating system, remote/cloud workspace, language, or codebase. The workflow provides review and verification discipline; it cannot guarantee maximum-quality output or establish better quality per token from the current evaluations.

The initial findings below are retained to explain the release decision. Their status lines and current result record the post-fix state. The original audit predated the public repository; no tagged release was created by this review.

## Scope and method

- Inspected the complete installable skill: instructions, conditional references, templates, UI metadata, optional reviewer configuration, and Python provenance helper.
- Inspected package validator/tests, installation/publication documentation, CI, development requirements, and retained evaluation artifacts.
- Used a fresh independent security reviewer plus coordinator confirmation of the principal issue. Model identity is unknown; no cross-model claim.
- Native host: Codex CLI `0.154.0-alpha.6.2` from the desktop installation, macOS, Python 3.11.1, Git 2.54.0.
- Used actual `codex app-server` `skills/list` requests against isolated projects; no user-owned Codex tasks were created and no model inference was needed for discovery.
- Security probes used disposable repositories and harmless local marker files. No credentials or production services were used.
- Snapshot hashes and sanitized machine-readable results accompany this report under `evals/publication-audit-2026-09-20/`.

The installed security-review skill's linked auxiliary playbook is missing, and the Python security references cover web frameworks rather than this CLI. Review therefore used the available skill checklist and a scoped local-tool threat analysis; this is not an OWASP/ASVS certification.

## Findings

### SEC-001 — Medium, high confidence: Git can execute a remote helper during provenance capture

**Location:** [review_evidence.py](../skills/production-engineering-loop/scripts/review_evidence.py), lines 22–28 and 46–47.

The wrapper disables `core.fsmonitor`, but still permits Git lazy fetching. Resolving a missing promised base object can initiate a fetch and execute a repository-configured remote helper. This violates the helper's stated no-network/no-repository-execution boundary even though it ultimately reports a capture error.

**Reproduction:** In an isolated repository, create two commits; remove the base commit object; configure `remote.origin.promisor=true`, `remote.origin.url=ext::<harmless marker script>`, and `protocol.ext.allow=always`; run `capture --base <missing-base>`. Both independent reviewer and coordinator runs observed **marker executed: true**, followed by exit 2 (`rev-parse` error). The marker script only wrote a sentinel in scratch storage.

**Preconditions/impact:** The selected repository must have relevant local Git configuration and a missing promised object. An ordinary tracked source file in a clean clone does not alone establish this condition. In the reproduced configuration the supposedly offline helper executes a configured program; normal partial-clone configurations can also perform unintended network activity. Installation itself does not run the helper.

**Required correction:** Force offline behavior in every Git subprocess, preserving existing caller environment while overriding `GIT_NO_LAZY_FETCH=1` and denying transports (`GIT_ALLOW_PROTOCOL=''`). The reviewer verified these mitigations on Git 2.54.0. Test supported Git versions, and retain explicit failure/manual-evidence fallback for unavailable objects. Add capture/check/validate regressions using a missing promised object and a harmless executable sentinel. An exit error alone must not count as safe failure if the sentinel ran.

**Status:** Resolved and independently rechecked. All helper Git subprocesses override inherited settings with lazy fetching and transports disabled. The regression exercises `capture`, `check`, and `validate`; all fail with exit 2 and leave the marker absent when the required object is unavailable.

### PUB-002 — Low, high confidence: personal paths in historical evidence

Four personal-home-directory occurrences were found in three files:

- `evals/review-loop-2026-09-20/candidate-evidence/stale-probe.log:1`
- `evals/review-loop-2026-09-20/candidate-refactor-review-evidence/review-report.json:30`
- Same report at line 62.
- `evals/review-loop-2026-09-20/candidate-review-evidence/review-report.json:55`

These disclose a local account/workspace location, not an observed credential. None occur in the installable skill package. Before making the whole repository public, create explicitly sanitized public evidence copies or exclude the affected artifacts; retain original evidence privately rather than silently presenting edited logs as original captures.

**Status:** Resolved for the candidate public repository. The occurrences were replaced with explicit portable placeholders and labeled as sanitized evidence. A repository-wide repeat scan found no personal home paths.

### PUB-003 — Immutable release verification remains

- The public repository is `NagarjunMa/production-engineering-skills`, and installation from its public `main` branch is verified.
- No immutable release tag has been verified, so release-specific installation and rollback evidence remain pending.
- The CI matrix and dependency-update configuration are present. Hosted run 35556792913 passed on public `main` commit `a58818220c8f59fd1717457b73758ef1f0018462`; no equivalent result is yet associated with an immutable release.

These are release-state gaps rather than code defects. The maintainer must tag the reviewed snapshot, observe its configured CI, and test the exact tagged download before making the corresponding release claim.

## Verified compatibility

| Capability | Actual observation |
| --- | --- |
| Project installation | Skills CLI found exactly one skill and copied it into a fresh project's `.agents/skills/production-engineering-loop`; the installed files matched the source and Codex returned scope `repo`, enabled `true`, with correct display metadata |
| Nested-directory discovery | The same project skill was found when the working directory was a nested child |
| Personal installation across projects | The existing personal symlink was returned as scope `user`, enabled `true`, in two unrelated fresh Git projects with no project skill copy |
| Package integrity | Existing package validator passed all bundled links, metadata, and license consistency |
| Native prompt metadata | `codex debug prompt-input` included the skill metadata; it did not inline the body in that diagnostic. This proves visibility, not model selection or execution |
| Engineering workflow | Earlier retained v0.5 worker/refactor/fallback trials demonstrate bounded instruction execution and delegated review; they do not cover arbitrary languages/projects |
| Optional helper | The suite now includes the promised-object/remote-helper boundary and passes; the independent positive control proves the probe can detect execution |

The disposable project contained both project and personal copies during the precedence check, and Codex listed both. This was intentional for the test; users should normally choose one scope to avoid overlapping versions.

Official sources checked on 2026-09-20: [Codex skills](https://learn.chatgpt.com/docs/build-skills) documents project `.agents/skills` and personal `~/.agents/skills` discovery, including symlinks. [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) documents optional reviewer configuration. Current guidance recommends plugin packaging for reusable public distribution. A direct skill folder still works locally; absence of a plugin manifest does not invalidate the tested local install. A directory-listed plugin would need separate packaging and publication verification.

## Security checks and limitations

- Positive controls: no install hook, required MCP server, runtime third-party dependency, hardcoded account path, automatic deployment command, or package-controlled credential upload found in the installable package.
- Instructions preserve user authority, keep review-only work read-only, bound review rounds, separate claimed model identity from observed identity, and retain pending review when required capabilities are unavailable. Instructions are not a sandbox.
- Existing fsmonitor isolation regression passed. Additional probes passed parent-symlink escape rejection, contract traversal rejection, Git-metadata path rejection, FIFO refusal without blocking, existing-output overwrite refusal, and inert command strings in reports. Malformed reports failed cleanly in exercised cases.
- Limited signature scan: 231 text files, no private-key/GitHub/AWS/OpenAI/Slack token-pattern matches. No entropy-based secret scanner was available; this is not proof of absence of all secrets. There is no commit history to scan.
- `pip-audit -r requirements-dev.txt` found no known vulnerabilities in the pinned development dependency, PyYAML 6.0.3. The optional helper uses the standard library.
- Docker server was unavailable. The later hosted CI run exercised the package checks on Linux and Windows and Python 3.10, but no interactive native host workflow was exercised there. No clean-account global install, live TOML reviewer-role load, cross-model run, remote/cloud install, or real GitHub release download was performed in this audit.
- No native automatic model-selection guarantee follows from discovery. Available models, tools, organizational policy, repository commands, and permissions determine what can actually execute.

## Recommended public claim and release gate

A defensible description is: **A portable Agent Skill for Codex, Claude Code, Cursor, Gemini CLI, Qwen Code, and OpenCode that guides implementation, architecture review, evidence-backed verification, and reusable project knowledge. Package installation is verified across these targets; end-to-end task behavior is currently verified most deeply on Codex.** Avoid promises of perfect code, equivalent behavior on every model, universal compatibility, security certification, or maximum quality per token. Existing matched trials did not establish improved defect detection or measured token efficiency over the baseline.

Before community release:

1. Create an immutable release from a reviewed revision and observe the configured hosted checks for that release revision.
2. Install that exact release in fresh destinations for the six documented host targets; confirm package equality and record native discovery results separately.
3. Enable the repository's private vulnerability-reporting route.
4. Publish the tested support statement and keep unexercised task behavior, cloud environments, and organization-specific configurations labeled as unverified until their runs are recorded.

**Release status: Local v0.6 candidate.** Installation from the previous public `main` works and hosted CI passed for public v0.5 commit `a58818220c8f59fd1717457b73758ef1f0018462`. The local v0.6 package passes its current checks and multi-host installation test, but its commit, hosted CI, immutable release, and broader host task evaluations remain pending. No unresolved local implementation defect was found.
