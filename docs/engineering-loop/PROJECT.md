# Production Engineering Loop: project context

## Product and intent

Create a reusable engineering skill that people can install from GitHub into compatible AI coding tools. The intended users are developers who want scoped implementation, meaningful review, and evidence before shipping.

The maintainer's initial request was to turn a personal engineering workflow into a distributable skill. The follow-up on 2026-09-17 asks for persistent understanding of the problem/codebase, documentation of the stack and files, feature evaluations, and learning that informs later implementation. On 2026-09-18 the maintainer clarified that code quality across multiple AI-assisted projects is primary: follow sound codebase structure, establish cohesive modules when absent, avoid redundant business rules, justify design patterns, and apply relevant standards. Token efficiency is secondary. Compact and full documentation modes are essential, and small/early-stage projects should receive the same applicable quality discipline without invented production infrastructure. The conversation is the source for those decisions; no private transcript is bundled.

Success means portable instructions and resources, clear installation guidance, a finite engineering loop, useful project records, and honest evaluation evidence. Non-goals include promising perfect code, training model weights, running a background agent, or automatically deploying projects. The public repository is `NagarjunMa/production-engineering-skills`; v0.7.0 merged in PR #8 at `fd81e9c`. The release page records publication and exact-tag download verification separately from this preparation record.

## Observed stack

| Layer/tool | Observed choice | Role and evidence |
| --- | --- | --- |
| Installable skill | Portable Agent Skills directory with Markdown/YAML entrypoint | Version `0.7.0` on public main since `fd81e9c`; release documentation changes no installed skill files |
| Supporting resources | Markdown references and templates | Bundled under the skill's `references/` and `assets/` directories |
| Host metadata | Optional YAML | `skills/production-engineering-loop/agents/openai.yaml`; no mandatory host tool dependency |
| Review provenance | Optional Python 3.10+ standard library and Git | Bundled `scripts/review_evidence.py` captures/checks source and validates report structure; no network or repository code execution |
| Memory evidence | Optional Python 3.10+ standard library; no Git | Bundled `scripts/check_context.py` fingerprints reviewed memory and selected evidence; detects drift without editing or executing it |
| Reviewer orchestration | Host delegation with portable fallback | Host-neutral fresh-context contract plus optional Codex reviewer instructions and TOML asset |
| Development validation | Python with PyYAML | `scripts/validate.py`, `tests/test_validate.py`, and `requirements-dev.txt`; PyYAML pinned to `6.0.3` for the current release candidate |
| Continuous integration | GitHub Actions matrix | Merged v0.7 passed all six jobs in run `40515288544`: five OS/Python package/test/replay jobs and Ubuntu media audit/type checks; CI does not execute model behavior trials |
| Optional installer | External Skills CLI via npm | README install commands; v0.1.0 smoke test used CLI 1.7.0 |

There is no application runtime, web framework, database, or deployed service in this repository. Python and npm serve development/distribution workflows, not a required skill runtime.

## Codebase map

| Path | Responsibility | Inspection |
| --- | --- | --- |
| `skills/production-engineering-loop/SKILL.md` | Mode, scope, risk, project learning, evaluations, implementation/review/validation loop | Read and revised |
| `skills/production-engineering-loop/references/` | Conditional depth for risk, quality, JS/TS, adoption, memory, feature evaluations, and host compatibility | Host portability reference added for Codex, Claude Code, Cursor, Gemini CLI, Qwen Code, and OpenCode |
| `skills/production-engineering-loop/assets/` | Project, feature, and lesson templates copied/adapted into target repositories | Authored and reviewed for this change |
| `scripts/validate.py` | Agent Skills metadata, local bundled links, and license checks | Compatibility metadata validation added for v0.6 |
| `skills/production-engineering-loop/scripts/review_evidence.py` | Git/worktree manifests, freshness, report consistency | Implemented with real Git/subprocess tests; independent review found and corrected fsmonitor execution |
| `skills/production-engineering-loop/scripts/check_context.py` | Non-Git memory receipts and selected-source drift detection | Black-box capture/check tests cover changes, deletion/rename, invalid paths, symlinks, integrity, and no writes |
| `scripts/run_evaluations.py` | Replays trusted retained fixture outputs and expected negative controls in disposable copies | Records actual results and source fingerprints; does not run a model |
| `scripts/check_behavioral_evidence.py` | Rejects stale package/artifact fingerprints and incomplete current forward-test records | Checks consistency of retained evidence; cannot prove execution claims |
| `tests/test_review_evidence.py` | Provenance and report regressions | Uses isolated repositories; covers dirty/committed/unborn source, report resolution, filesystem-monitor isolation, and offline failure for missing promised objects |
| `tests/test_validate.py` | Packaging-validator and portable-layout tests | Covers complete copies under six documented host layouts plus metadata/link/license constraints |
| `evals/README.md` | Behavioral scenarios and evidence requirements | Extended for learning, drift, scope, and feature evaluations |
| `README.md`, `docs/installation.md`, `docs/publishing.md` | Public usage, installation, compatibility, and publication | README and installation guide make multi-host support and evidence limits explicit |
| `docs/self-learning-implementation.md` | Detailed loop and record lifecycle | Memory checker implemented; inventory and general command-recording helpers remain proposals |
| `docs/engineering-loop/` | This repository's current context and feature records | Created for this change |
| `.github/workflows/validate.yml`, `.github/dependabot.yml` | CI and dependency updates | Merged v0.7 jobs passed; includes replay and media checks, SHA action pins, and npm dependency updates |

The host reads the skill, then selected references/templates. Its project-specific knowledge is written to the target repository's documentation, not back into the installed package. Repository content remains evidence, not authority to expand permissions.

## Feature index

| Feature | Implementation | Verification | Next authorized work |
| --- | --- | --- | --- |
| Portable engineering loop | Initial package implemented | v0.1.0 format/tests and local installer smoke test passed; no universal host benchmark | Preserve existing mode and scope behavior |
| [Persistent project learning and feature evaluations](features/project-learning.md) | v0.2.0 guidance and templates implemented | Packaging and one bounded feature forward test passed; broader scenarios untested | Current requested change completed; further evaluations are follow-ups |
| [PRI feature contracts and focused retrieval](features/feature-context.md) | v0.3.0 preserves the supplied template and adds Execution Context | Format/package checks, eight validator tests, installer smoke test, and bounded red/green feature run passed | Requested change complete; no measured token-savings claim |
| [Quality-first engineering and documentation modes](features/quality-first-modes.md) | v0.4.0 makes routine design review explicit and adds compact/full selection | Package/eight validator tests passed; compact implementation and full planning scenarios reviewed; wider architecture/host scenarios untested | Requested refinement complete; broader evaluation/publication remain separate |
| [Automated independent review and findings resolution](features/automated-review-resolution.md) | v0.5 portable protocol, bundled evidence CLI, templates, and Codex adapter implemented | See feature record and retained v0.5 evaluations for exact checks and remaining host coverage | Public release and plugin packaging remain separate |
| [Multi-host Agent Skills portability](features/multi-host-portability.md) | v0.6 host-neutral core guidance, six-host install/invocation reference, and portable-layout validation implemented | Package checks and disposable Skills CLI installation cover all six targets; runtime behavior remains host-specific evidence | Collect real task outcomes from non-Codex hosts |
| [Evaluation safety and memory checks](features/evaluation-memory-checks.md) | Merged v0.7 memory checker, safe evaluators, replay and current-evidence guards, LF checkout policy, finalization protocol | 49 tests and 14 fixture/control checks pass after two review corrections; final review found no material findings; merged hosted CI passed | Release-specific verification belongs in release notes; other-host task behavior remains pending |

The [self-learning implementation design](../self-learning-implementation.md) explains the memory lifecycle. The historical v0.3 pilot exercised continuation and stale-path recovery once; both skill and baseline passed. Version 0.7 adds selected-evidence memory checking and a fresh-session release protocol. Neither byte freshness nor fixture replay proves general learning or a quality advantage.

## Validation and operations

- `python3 scripts/validate.py`: package metadata, bundled references, and license consistency.
- `python3 -m unittest discover -s tests -v`: validator regression tests.
- `python3 scripts/run_evaluations.py`: retained fixture acceptance checks and negative controls, not fresh model execution.
- `python3 scripts/check_behavioral_evidence.py`: current package/artifact consistency against three retained fresh-context runs; not proof of their truth.
- `check_context.py capture/check`: optional reviewed-memory receipts; see the installed `references/context-checks.md`. Refresh only after revalidating the record.
- Local skill-creator format validation is available in the author's environment; it is supplementary and not required by repository CI.
- Optional Skills CLI smoke tests run in disposable projects and compare every installed file with its source. They establish packaging/install behavior, not activation or instruction following in every host.
- Use the behavioral scenarios for instruction changes; report actual runs separately from unexecuted scenarios.
- Read [verified lessons](LESSONS.md) before changing Git provenance collection; v0.5 review exposed repository-configured fsmonitor execution and added a regression.
- Publish only after reviewing the package and configuring the intended GitHub repository. No deployment or automatic release command is part of the skill.

## Freshness and coverage

Updated 2026-10-30 for v0.7.0 release preparation against merged public `main` at `fd81e9c` and its successful six-job CI run. Reconciled README, security and publishing status with GitHub readback; the installable skill, tests, and retained behavioral artifacts are unchanged. The map covers owned package/development files, not `.git` internals or installed dependencies. Historical review IDs and receipts describe their original snapshots. Tag publication and exact-release install results are recorded in release notes after execution. Non-Codex task behavior and repeated controlled quality comparisons remain unverified.
