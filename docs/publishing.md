# Publication and release checks

The repository is public. Version 0.7.0 was merged in PR #8 at `fd81e9c` on 2026-10-27 and passed all six [hosted validation jobs](https://github.com/NagarjunMa/production-engineering-skills/actions/runs/40515288544). The v0.7.0 release reconciles documentation without changing the evaluated skill package. The [release page](https://github.com/NagarjunMa/production-engineering-skills/releases/tag/v0.7.0) records publication status and release-specific verification; historical pre-merge receipts remain unchanged.

1. Review the skill, README, and MIT license, including the copyright attribution.
2. Use the selected public repository, `NagarjunMa/production-engineering-skills`, and keep the README install command aligned with it.
3. Run the package validator, unit tests, `python3 scripts/run_evaluations.py`, and `python3 scripts/check_behavioral_evidence.py`. Follow `evals/loop-2026-10-26/README.md` for new fresh-agent evidence after instruction changes; never refresh fingerprints in place of rerunning. Keep fixture replay, live behavior, and matched quality comparisons separate. Run the disposable multi-host installer check and state which agents/versions were actually tested.
4. Inspect the files being committed for private material. Add a remote for the selected repository, commit the reviewed contents, and push when ready.
5. The previous public `main` installation was tested in a disposable Codex project. After creating an accepted release, repeat installation against its exact immutable tag/commit for the documented host targets and confirm that every installed package matches it. Record native discovery separately from installation.
6. Tag the exact accepted commit after required CI passes. Package metadata is `0.7.0`; keep tag and metadata consistent. Do not move an existing release tag. Describe known limitations without claiming equal behavior across hosts, defect-free output, or measured quality-per-token improvement.

The public repository and branch installation are established. Record tag/commit, exact-release download/install checks, host/version, and any discovery or invocation evidence in the release notes. Do not infer those outcomes from branch installation or CI. Marketplace listing and behavioral verification in every coding agent are not established.
