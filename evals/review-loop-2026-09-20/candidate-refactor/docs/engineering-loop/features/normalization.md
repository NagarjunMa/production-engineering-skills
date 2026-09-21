# Tag normalization refactor
Compact mode: bounded Standard behavior-preserving consolidation; fresh review required because shared rules materially change. Contract: README.md and AGENTS.md; no issue ID or external integration target supplied.

Execution Context: adapters.py web_tag/cli_tag, helpers.py normalize_tag, plugins.py run_registered and deployment/registry.json inspected. Dynamic symbol_parts select normalize_tag; retain export. Initial two happy-path tests pass. Completed: four characterization tests passed before consolidation; adapters now reuse helper. Next: final native gate and fresh-review evidence in sibling candidate-refactor-evidence. No unresolved implementation decision.

AC1: whitespace stripping, lowercase and empty rejection remain identical. Characterize normal, empty, whitespace, Unicode across adapters/helper/plugin. Wrong implementation uppercases or skips empty rejection; explicit expected output catches it.
AC2: independent adapters retain HTTP 422 nested data versus CLI status 2/plain message and success formats. Wrong implementation unifies shape; distinct expected tuples catch it.
AC3: helper public export remains usable and manifest dispatch works. Wrong dead-code removal breaks direct import or dynamic dispatch test. Structural inspection must establish one canonical normalization rule without hiding duplicate logic behind wrappers.
AC4: full native gate and required fresh review complete without unresolved material findings.

Design: reuse helpers.normalize_tag; adapters catch ValueError and translate to their independently specified contracts; plugins remains unchanged. No new architecture or dependencies. Tests derive expected outputs literally rather than importing production normalization for expectations.

Verification: pure refactor; passing characterization before/after, no intended red behavior change. Command: python3 -m unittest discover -s tests -v. Source inspection complements tests for removed duplication and retained contracts. Local-only work, no mutation of external systems.

Compatibility: public symbols and dynamically selected helper unchanged. No migration, deployment or release. Rollback adapters.py together if necessary; no persisted state. Scoped lesson applies here: verify dynamic manifest consumers before deleting apparently unused public helpers.

Actual changes: adapters.py now calls canonical helper and maps errors per adapter. Added tests/test_contracts.py and repository-owned project/feature memory. helpers.py, plugins.py, deployment registry, README and AGENTS untouched. All source inspected; unknown external consumers and runtimes remain unverified. Final snapshot and verdict are recorded externally to avoid self-invalidating evidence.
