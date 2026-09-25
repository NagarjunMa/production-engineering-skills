# Initial publication

The repository is prepared locally. Creating a public GitHub repository, pushing it, and publishing a release are separate actions for the maintainer.

1. Review the skill, README, and MIT license, including the copyright attribution.
2. Use the selected public repository, `NagarjunMa/production-engineering-skills`, and keep the README install command aligned with it.
3. Run the package validator and its tests using the commands in the README. Run the disposable multi-host installer check, then exercise representative behavioral scenarios and state which agents/versions were actually tested.
4. Inspect the files being committed for private material. Add a remote for the selected repository, commit the reviewed contents, and push when ready.
5. The previous public `main` installation was tested in a disposable Codex project. After creating a v0.6 release, repeat installation against that exact immutable release for the documented host targets and confirm that every installed package matches it. Record native discovery separately from installation.
6. Tag a release when its contents are accepted. The current metadata version is `0.6.0`; keep the tag and skill metadata consistent. Describe known limitations without claiming equal behavior across hosts, defect-free output, or measured quality-per-token improvement.

The public repository and remote installation are established. A hosted release, immutable release-download test, and marketplace listing are not yet assumed by this package.
