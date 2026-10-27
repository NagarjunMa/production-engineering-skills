# Publication and release checks

The repository is public. Main at `4501e91` contains v0.6.0; v0.7.0 is under local verification. Pushing these changes and publishing an immutable release remain separate actions.

1. Review the skill, README, and MIT license, including the copyright attribution.
2. Use the selected public repository, `NagarjunMa/production-engineering-skills`, and keep the README install command aligned with it.
3. Run the package validator, unit tests, `python3 scripts/run_evaluations.py`, and `python3 scripts/check_behavioral_evidence.py`. Follow `evals/loop-2026-10-26/README.md` for new fresh-agent evidence after instruction changes; never refresh fingerprints in place of rerunning. Keep fixture replay, live behavior, and matched quality comparisons separate. Run the disposable multi-host installer check and state which agents/versions were actually tested.
4. Inspect the files being committed for private material. Add a remote for the selected repository, commit the reviewed contents, and push when ready.
5. The previous public `main` installation was tested in a disposable Codex project. After creating an accepted release, repeat installation against its exact immutable tag/commit for the documented host targets and confirm that every installed package matches it. Record native discovery separately from installation.
6. Tag a release when its contents are accepted. Local metadata is `0.7.0`; keep tag and metadata consistent. Describe known limitations without claiming equal behavior across hosts, defect-free output, or measured quality-per-token improvement.

The public repository and remote installation are established. A hosted release, immutable release-download test, and marketplace listing are not yet assumed by this package.
