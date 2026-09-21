# Codex compatibility and publication security audit

**Date:** 2026-09-20  
**Package:** `skills/production-engineering-loop`, version 0.5.0  
**Verdict:** **Local release candidate.** The reproduced helper defect and publication-hygiene findings are resolved; a real GitHub release, hosted CI execution, and install from that immutable release remain external publication steps.

## Current result

The repository was hardened after this audit at the maintainer's request:

- SEC-001: fixed locally. Every helper Git subprocess now forces `GIT_NO_LAZY_FETCH=1`, `GIT_ALLOW_PROTOCOL=''`, `GIT_TERMINAL_PROMPT=0`, and `GIT_OPTIONAL_LOCKS=0`, while retaining filesystem-monitor isolation. A new regression removes a promised base object and verifies that `capture`, `check`, and `validate` all fail without executing the configured remote helper.
- PUB-002: fixed in the candidate public artifacts. The four personal paths were replaced with explicit portable placeholders and marked as sanitized evidence. The installable package continues to contain no personal home paths.
- PUB-003: all local preparation is complete. Version documentation matches 0.5.0, the development dependency is pinned, CI actions are pinned to immutable revisions, Dependabot is configured, and CI covers Ubuntu Python 3.10–3.12 plus macOS/Windows Python 3.11. Hosted execution and installation from the future public URL remain impossible until the maintainer creates and publishes that repository.

Local package validation, skill-format validation, dependency audit, and 27 tests pass after these changes. An independent return review reproduced the original hostile setup: an unguarded positive control executed its harmless marker, while the corrected helper's `capture`, `check`, and `validate` commands each failed closed without executing the marker. The reviewer also verified hostile inherited Git environment values were overridden.

The skill can be installed once at personal scope and used across local projects. A project copy also works, including discovery from a nested directory. That does not establish compatibility with every Codex version, organization policy, operating system, remote/cloud workspace, language, or codebase. The workflow provides review and verification discipline; it cannot guarantee maximum-quality output or establish better quality per token from the current evaluations.

The initial findings below are retained to explain the release decision. Their status lines and current result record the post-fix state. No GitHub repository, release, or hosted execution was created by this local audit.

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

### PUB-003 — External publication verification remains

- README intentionally contains `YOUR_GITHUB_OWNER` because no public repository identity has been selected locally.
- No remote, initial repository commit, immutable release tag, or actual public install URL exists, so a fresh GitHub download cannot yet be verified.
- The CI matrix and dependency-update configuration are present, but hosted jobs have not run.

These are external release-state gaps rather than code defects. The maintainer must select the repository, publish the reviewed snapshot, observe the configured CI, and test the exact tagged download before making the corresponding release claim.

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
- Docker server was unavailable. No Linux/Windows native run, Python 3.10 runtime run, clean-account global install, live TOML reviewer-role load, cross-model run, remote/cloud install, or real GitHub release download was performed in this audit.
- No native automatic model-selection guarantee follows from discovery. Available models, tools, organizational policy, repository commands, and permissions determine what can actually execute.

## Recommended public claim and release gate

A defensible description is: **A Codex-compatible engineering workflow that guides implementation, architecture review, evidence-backed verification, and reusable project knowledge.** Avoid promises of perfect code, universal compatibility, security certification, or maximum quality per token. Existing matched trials did not establish improved defect detection or measured token efficiency over the baseline.

Before community release:

1. Create an immutable release from this reviewed candidate and observe the configured hosted checks.
2. Install that exact release in a fresh destination and confirm Codex discovery.
3. Replace the owner placeholder and enable the real repository's private vulnerability-reporting route.
4. Publish the tested support statement and keep Windows, cloud environments, and other agents labeled as unverified until their runs are recorded.

**Release status: Local release candidate.** The remaining gates require the future public repository or external environments; no unresolved local implementation defect was found.
