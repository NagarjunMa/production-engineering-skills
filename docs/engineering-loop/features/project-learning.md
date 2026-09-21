# Feature: persistent project learning and feature evaluations

## Contract

Source: maintainer's 2026-09-17 request to read the problem or codebase, document product/stack/files, retain useful context, develop evaluations per feature, and implement accordingly.

Implement portable skill instructions and bundled templates for this workflow. Preserve review-only mode, narrower file scopes, and explicit verification limits. Non-goals: automatic background execution, model training, unrequested backlog implementation, or silently modifying the installed skill from project lessons.

Risk: significant workflow change, because persisted context and evaluation criteria influence future edits across tasks. No change to production infrastructure, credentials, or permissions is included.

## Acceptance and evaluation plan

| ID | Criterion | Method | Status |
| --- | --- | --- | --- |
| A1 | Read product intent, inventory the project, and distinguish observed stack/files from plans and inspection gaps | Inspect bootstrap instructions/templates; bounded greenfield forward test | Passed for the small greenfield fixture; large existing-codebase coverage untested |
| A2 | Retain context in the target repository; refresh stale facts and preserve review-only/narrow scopes | Inspect memory lifecycle and scope rules; dedicated scenarios in `evals/README.md` | Static review complete; multi-session/drift scenarios not run |
| A3 | Define feature criteria and independent expected outcomes before implementation; record actual evaluations | Inspect evaluation reference/template; bounded feature build and independent checks of produced code | Passed for the fixture; evaluation-first chronology reported by evaluator |
| A4 | Update actual files/status and learn only from evidenced outcomes without rewriting the skill | Inspect completion rules/templates and forward-test artifacts | Actual records updated; no unsupported lesson invented; learning from a failure not tested |
| A5 | Ship all new references/templates as a self-contained package | Package validator, skill-format validator, validator tests, disposable installation and file comparison | Passed: both format checks, eight tests, complete 12-file installed copies |

The feature contract was documented during this revision after the initial instruction edits; this record does not claim a test-first development history for the skill itself. The updated skill directs future feature work to establish criteria before implementation.

## Actual files created or changed

| Path | Action | Purpose |
| --- | --- | --- |
| `skills/production-engineering-loop/SKILL.md` | Change | Integrate memory, evaluation planning, and evidence-based learning; metadata version 0.2.0 |
| `skills/production-engineering-loop/references/project-learning.md` | Create | Bootstrap, resume, drift resolution, file mapping, and bounded lessons |
| `skills/production-engineering-loop/references/feature-evaluations.md` | Create | Acceptance-derived evaluations, independent expectations, and outcome-driven improvements |
| `skills/production-engineering-loop/assets/project-template.md` | Create | Product, stack, codebase map, features, and coverage |
| `skills/production-engineering-loop/assets/feature-template.md` | Create | Contract, checks, actual file changes, results, and handoff |
| `skills/production-engineering-loop/assets/lesson-template.md` | Create | Evidence, applicability, regression checks, and supersession |
| `skills/production-engineering-loop/references/repository-adoption.md` | Change | Team-owned context without private-memory dependencies |
| `skills/production-engineering-loop/agents/openai.yaml` | Change | Invocation text reflecting project context and feature evaluations |
| `README.md`, `CONTRIBUTING.md`, `docs/installation.md`, `docs/publishing.md` | Change | Usage, maintenance, template installation, new-version evidence, and release guidance |
| `evals/README.md` | Change | Add eight learning/evaluation scenarios |
| `evals/learning-loop-result.md` | Create | Record independent forward-test conditions, reviewed evidence, and limits |
| `docs/engineering-loop/PROJECT.md` and this file | Create | Concrete project context and implementation evidence for this repository |

The repository is entirely uncommitted from initial creation; “change” describes this turn's edits to the prior working-tree version, not a committed Git diff. Existing validator code and tests are unchanged.

## Evaluation runs

Current source: 2026-09-17 working tree, skill metadata 0.2.0, no commit. Results from the previous 0.1.0 package are not reused as evidence for new resources.

| Check | Result | Scope and limitations |
| --- | --- | --- |
| `python3 scripts/validate.py` | Passed | Metadata, bundled reference/template links, license consistency |
| `python3 -m unittest discover -s tests -v` | Passed: 8 tests | Packaging-validator regression cases; not instruction-following tests |
| Skill-creator `quick_validate.py` against this package | Passed | Supplemental skill-format check; requires the author's local skill-creator installation |
| Disposable Skills CLI installation targeting five agents with `--copy --yes` | Passed | All 12 package files matched in `.agents/skills` and `.claude/skills`; host activation not tested |
| Repository Markdown links, whitespace, and UI metadata inspection | Passed | Local static check; no claim of remote-link availability |
| Independent greenfield stock-adjustment feature build | Passed within bounded scope | Seven generated tests passed; project and feature records inspected; no unsupported lesson invented |
| Parent's independent feature verification | Passed | 168 bounded quantity/delta cases plus missing-product atomicity; generated test suite also rerun |

See the [forward-test result](../../../evals/learning-loop-result.md) for setup, artifact evidence, and untested scenarios.

## Handoff

- Implementation: instructions, references, and templates created.
- Verification: packaging checks and one bounded independent feature build passed; broader behavioral coverage remains limited as described above.
- Release: not published.
- Remaining coverage: full multi-session learning, stale-memory handling, and host-specific activation remain unverified until their scenarios run.
- Lessons: no reusable failure has been established for this feature yet; no lesson file is created merely to fill the structure.
