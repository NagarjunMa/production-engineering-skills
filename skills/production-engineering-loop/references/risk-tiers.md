# Risk Tiers

Choose the highest tier matched by the changed behavior. Scope validation to credible failure modes, not file count or keywords alone. Copy edits mentioning a critical subsystem remain trivial when they do not change its behavior, policy, or operating instructions.

## Classification

| Tier        | Typical changes                                                                                                                                                                                       | Minimum evidence                                                                                                                                                                  |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Trivial     | Copy, comments, or documentation with no executable, policy, contract, or operational effect                                                                                                          | Inspect the diff and run a relevant formatter or documentation check when available                                                                                               |
| Standard    | Localized implementation or configuration inside one established boundary                                                                                                                             | Focused automated tests, static checks for the changed language, and regression review                                                                                            |
| Significant | Public API or schema contracts, external integrations, shared libraries, caching, concurrency, performance-sensitive paths, releases, or changes spanning boundaries                                  | Focused tests plus integration or contract coverage, full affected-subsystem checks, compatibility and rollback analysis, and measurements for material efficiency claims         |
| Critical    | Authentication, authorization, billing, payments, migrations, row-level security, secrets, permissions, destructive operations, production data, security controls, or untrusted agent/tool execution | Significant-tier evidence plus explicit additional review, negative/adversarial cases, manual or sandbox verification where applicable, and documented rollout and rollback gates |

## Risk Amplifiers

Raise the tier when any of these are present:

- large user or data blast radius;
- irreversible or difficult rollback;
- ambiguous ownership or incomplete requirements;
- untrusted input crossing into privileged execution;
- compatibility with independently deployed clients;
- silent data corruption or billing risk;
- high-frequency, memory-sensitive, or cost-sensitive execution;
- weak observability or no representative test environment.

## Validation Selection

For every tier:

1. Map each acceptance criterion and material failure mode to evidence.
2. Prefer the smallest test that proves the behavior, then run required repository gates.
3. Test negative paths at trust boundaries, not only the successful path.
4. Record why an unavailable check is blocked and how the risk will be handled.

Critical classification does not authorize a production mutation or invalidate existing authorization. Finish safe in-scope implementation and validation. Before release, obtain an explicit additional review by a qualified human or an independent reviewer where permitted, and satisfy the repository's release gates. If that review is unavailable, report release readiness as pending; do not substitute repeated self-review for independent approval.
