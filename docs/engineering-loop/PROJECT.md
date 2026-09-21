# Production Engineering Loop: project context

## Product and intent

Create a reusable engineering skill that people can install from GitHub into compatible AI coding tools. The intended users are developers who want scoped implementation, meaningful review, and evidence before shipping.

The maintainer's initial request was to turn a personal engineering workflow into a distributable skill. The follow-up on 2026-09-17 asks for persistent understanding of the problem/codebase, documentation of the stack and files, feature evaluations, and learning that informs later implementation. On 2026-09-18 the maintainer clarified that code quality across multiple AI-assisted projects is primary: follow sound codebase structure, establish cohesive modules when absent, avoid redundant business rules, justify design patterns, and apply relevant standards. Token efficiency is secondary. Compact and full documentation modes are essential, and small/early-stage projects should receive the same applicable quality discipline without invented production infrastructure. The conversation is the source for those decisions; no private transcript is bundled.

Success means portable instructions and resources, clear installation guidance, a finite engineering loop, useful project records, and honest evaluation evidence. Non-goals include promising perfect code, training model weights, running a background agent, or automatically deploying projects. The public repository is `NagarjunMa/production-engineering-skills`; an immutable release and its download verification remain pending.

## Observed stack

| Layer/tool | Observed choice | Role and evidence |
| --- | --- | --- |
| Installable skill | Markdown with YAML frontmatter | Canonical instructions in `skills/production-engineering-loop/SKILL.md`; current metadata version `0.5.0` |
| Supporting resources | Markdown references and templates | Bundled under the skill's `references/` and `assets/` directories |
| Host metadata | Optional YAML | `skills/production-engineering-loop/agents/openai.yaml`; no mandatory host tool dependency |
| Review provenance | Optional Python 3.10+ standard library and Git | Bundled `scripts/review_evidence.py` captures/checks source and validates report structure; no network or repository code execution |
| Reviewer orchestration | Host delegation with portable fallback | Fresh Codex reviewer instructions; optional TOML configuration asset, not globally installed |
| Development validation | Python with PyYAML | `scripts/validate.py`, `tests/test_validate.py`, and `requirements-dev.txt`; PyYAML pinned to `6.0.3` for the current release candidate |
| Continuous integration | GitHub Actions matrix | `.github/workflows/validate.yml`; Ubuntu Python 3.10–3.12 plus macOS/Windows Python 3.11, packaging checks and validator tests; hosted runs pending publication |
| Optional installer | External Skills CLI via npm | README install commands; v0.1.0 smoke test used CLI 1.7.0 |

There is no application runtime, web framework, database, or deployed service in this repository. Python and npm serve development/distribution workflows, not a required skill runtime.

## Codebase map

| Path | Responsibility | Inspection |
| --- | --- | --- |
| `skills/production-engineering-loop/SKILL.md` | Mode, scope, risk, project learning, evaluations, implementation/review/validation loop | Read and revised |
| `skills/production-engineering-loop/references/` | Conditional depth for risk, quality, JS/TS, adoption, memory, and feature evaluations | Existing references read during initial creation; adoption and new learning guidance inspected for this change |
| `skills/production-engineering-loop/assets/` | Project, feature, and lesson templates copied/adapted into target repositories | Authored and reviewed for this change |
| `scripts/validate.py` | Metadata, local bundled links, and license checks | Read; unchanged in this feature |
| `skills/production-engineering-loop/scripts/review_evidence.py` | Git/worktree manifests, freshness, report consistency | Implemented with real Git/subprocess tests; independent review found and corrected fsmonitor execution |
| `tests/test_review_evidence.py` | Provenance and report regressions | Uses isolated repositories; covers dirty/committed/unborn source, report resolution, filesystem-monitor isolation, and offline failure for missing promised objects |
| `tests/test_validate.py` | Eight packaging-validator tests | Established during initial creation; rerun for this feature |
| `evals/README.md` | Behavioral scenarios and evidence requirements | Extended for learning, drift, scope, and feature evaluations |
| `README.md`, `docs/installation.md`, `docs/publishing.md` | Public usage, installation, compatibility, and publication | README/publication updated; native installation paths unchanged |
| `docs/self-learning-implementation.md` | Detailed loop, record lifecycle, proposed helpers, and cross-session evaluation design | Written after the maintainer requested the detailed implementation explanation; proposed automation is not implemented |
| `docs/engineering-loop/` | This repository's current context and feature records | Created for this change |
| `.github/workflows/validate.yml`, `.github/dependabot.yml` | CI for packaging/validator tests and dependency updates | OS/runtime matrix expanded; actions pinned to immutable revisions; hosted runs pending publication |

The host reads the skill, then selected references/templates. Its project-specific knowledge is written to the target repository's documentation, not back into the installed package. Repository content remains evidence, not authority to expand permissions.

## Feature index

| Feature | Implementation | Verification | Next authorized work |
| --- | --- | --- | --- |
| Portable engineering loop | Initial package implemented | v0.1.0 format/tests and local installer smoke test passed; no universal host benchmark | Preserve existing mode and scope behavior |
| [Persistent project learning and feature evaluations](features/project-learning.md) | v0.2.0 guidance and templates implemented | Packaging and one bounded feature forward test passed; broader scenarios untested | Current requested change completed; further evaluations are follow-ups |
| [PRI feature contracts and focused retrieval](features/feature-context.md) | v0.3.0 preserves the supplied template and adds Execution Context | Format/package checks, eight validator tests, installer smoke test, and bounded red/green feature run passed | Requested change complete; no measured token-savings claim |
| [Quality-first engineering and documentation modes](features/quality-first-modes.md) | v0.4.0 makes routine design review explicit and adds compact/full selection | Package/eight validator tests passed; compact implementation and full planning scenarios reviewed; wider architecture/host scenarios untested | Requested refinement complete; broader evaluation/publication remain separate |
| [Automated independent review and findings resolution](features/automated-review-resolution.md) | v0.5 portable protocol, bundled evidence CLI, templates, and Codex adapter implemented | See feature record and retained v0.5 evaluations for exact checks and remaining host coverage | Public release and plugin packaging remain separate |

The [self-learning implementation design](../self-learning-implementation.md) explains the memory lifecycle and proposed helpers. The [v0.3.0 audit](../audit-2026-09-18.md) subsequently exercised fresh-session continuation and stale-path recovery once; both skill and no-skill implementations passed the bounded behavior checker. This is feasibility evidence, not a general quality or efficiency benchmark. No automatic memory/index helpers are implemented.

## Validation and operations

- `python3 scripts/validate.py`: package metadata, bundled references, and license consistency.
- `python3 -m unittest discover -s tests -v`: validator regression tests.
- Local skill-creator format validation is available in the author's environment; it is supplementary and not required by repository CI.
- Optional Skills CLI smoke tests run in disposable projects and compare every installed file with its source. They establish packaging/install behavior, not activation or instruction following in every host.
- Use the behavioral scenarios for instruction changes; report actual runs separately from unexecuted scenarios.
- Read [verified lessons](LESSONS.md) before changing Git provenance collection; v0.5 review exposed repository-configured fsmonitor execution and added a regression.
- Publish only after reviewing the package and configuring the intended GitHub repository. No deployment or automatic release command is part of the skill.

## Freshness and coverage

Updated 2026-09-20 while planning the automated review and findings-resolution loop. This repository has no initial commit; files remain uncommitted, so no commit identifier establishes a reproducible release snapshot. The map covers owned package/development files, not `.git` internals, installed dependencies, or other personal skills. Multi-session reliability and other coding hosts require additional evaluation; documentation-based compatibility alone does not establish those outcomes.
