# Initial publication

The repository is prepared locally. Creating a public GitHub repository, pushing it, and publishing a release are separate actions for the maintainer.

1. Review the skill, README, and MIT license, including the copyright attribution.
2. Create or select the intended GitHub repository. Replace `YOUR_GITHUB_OWNER` in the README with its actual owner; adjust the repository name if needed.
3. Run the package validator and its tests using the commands in the README. Exercise representative behavioral scenarios and state which agents/versions were actually tested.
4. Inspect the files being committed for private material. Add a remote for the selected repository, commit the reviewed contents, and push when ready.
5. Test the documented GitHub install command in a disposable project. Confirm that the skill and all references install and are discoverable in the selected host.
6. Tag a release when its contents are accepted. The current metadata version is `0.5.0`; keep the tag and skill metadata consistent. Describe known limitations without claiming universal compatibility, defect-free output, or measured quality-per-token improvement.

No GitHub account, repository owner, remote URL, hosted release, or marketplace listing is assumed by this package.
