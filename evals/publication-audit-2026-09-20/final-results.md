# Corrected local release-candidate results

Date: 2026-09-20, updated 2026-09-23 with local v0.6 portability evidence. Source state: reviewed local package with public remote; no immutable release has been verified.

## v0.6 portability update

- Package validator and Codex skill-format validator: passed.
- Python 3.11 test suite: 29 passed.
- Skills CLI targeted `codex`, `claude-code`, `cursor`, `gemini-cli`, `qwen-code`, and `opencode` in one disposable project.
- The resulting `.agents`, `.claude`, and `.qwen` copies each matched all 25 current source-package files byte for byte.
- OpenCode 1.18.27 discovered `production-engineering-loop` from the disposable project's `.agents/skills` directory without model execution.
- Claude Code 2.1.153 is installed locally, but native discovery and task behavior were not exercised in this update. Cursor, Gemini CLI, and Qwen Code runtimes were unavailable locally.
- These results establish format and installation portability. They do not establish equivalent task quality across hosts or models.

## Historical v0.5 results

- Package validator: passed.
- Codex skill-format validator: passed.
- Python 3.11 test suite: 27 passed.
- Python 3.12 review-helper suite: 16 passed.
- Development dependency audit: no known vulnerabilities in the pinned requirements.
- Local Skills CLI install: found exactly one skill, copied the package into a fresh project's `.agents/skills/production-engineering-loop`, and exited successfully.
- Fresh installed copy: byte-for-byte matched the source folder; Codex discovered one enabled repository-scoped `production-engineering-loop` skill.
- Public GitHub install: `NagarjunMa/production-engineering-skills` exposed exactly one skill; installation from public `main` succeeded, matched the local package, and was discovered by Codex.
- Hosted CI: [GitHub Actions run 35556792913](https://github.com/NagarjunMa/production-engineering-skills/actions/runs/35556792913) passed all five jobs for public `main` commit `a58818220c8f59fd1717457b73758ef1f0018462`: Ubuntu Python 3.10–3.12, macOS Python 3.11, and Windows Python 3.11.
- Standalone package inspection: 24 files, no symlinks, all bundled links valid; helper usable from unrelated scratch.
- Privacy and limited credential-signature scan: no personal home paths, private-key headers, or tested provider token patterns found.
- Independent security return review: `capture`, `check`, and `validate` each exited 2 on a missing promised base object and did not execute the configured remote-helper marker. The unguarded positive control executed the marker, proving the probe was effective. Hostile inherited `GIT_ALLOW_PROTOCOL` and `GIT_NO_LAZY_FETCH` values were overridden.

## Reviewed key hashes

```text
9727a8366462e95317f2395d90295f82ebb4ce3b520cb96c4983c4ba8ff0a850  skills/production-engineering-loop/scripts/review_evidence.py
e483824c5b32f6a9d3b44ee39be0a533795afb5e1d2b3494c5fd0e8fab7ccec6  tests/test_review_evidence.py
ba97784c41982069f52d9259b983550aa1f88ba4628bc8f3b66a868bbee49c19  tests/test_validate.py
b30b1430fbdf9784068b403cadc709715eb972cd935c5e017eeaaf46c0a5e18b  skills/production-engineering-loop/SKILL.md
975d5c4c5851ad203096b24414c02deb9dedd0e270433f7081f0d70aa37d2f8d  .github/workflows/validate.yml
f49ecb260a43e1b076b42a7db7453c4084d4b3bfe77d48f0225aceeb59cdc6c2  .github/dependabot.yml
e1309b264171fa41ad76e9ae8590cb8187e490db58d1415f0170fe163eabc200  SECURITY.md
```

Reviewer model identity was unknown, so this is an independent fresh-context review rather than a cross-model claim.

## External steps still unobserved

- An immutable tag/release and installation from that exact release.
- Private vulnerability reporting enabled on the selected repository.
- Broader projects, users, other coding agents, and cloud environments.

The hosted result validates the package checks on that public revision. It does not exercise an interactive coding-agent workflow on Linux or Windows and does not validate the current uncommitted documentation changes.
