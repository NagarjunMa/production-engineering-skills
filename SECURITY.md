# Security policy

## Supported version

The public default branch contains v0.6.0. The v0.7.0 changes are under local verification and are not yet released. No versioned GitHub release has been published. Report the exact commit and installation method when requesting a security fix; branch installations can change.

## Reporting a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/NagarjunMa/production-engineering-skills/security/advisories/new) for suspected vulnerabilities. The route was enabled and verified on 2026-10-26. Do not include real credentials, private customer data, or exploit activity against systems you do not own. A minimal synthetic reproduction, affected commit/version, impact, and suggested boundary are useful.

Do not open a public issue containing an unpatched vulnerability or exploit. If GitHub reporting is unavailable, request a working private contact without disclosing the vulnerability in public.

## Security boundary

Installing the skill loads instructions and bundled resources; it has no installation hook, background service, required network connection, API key, or MCP server. The optional `review_evidence.py` helper uses local Python and Git when invoked. Its Git subprocesses are forced offline and missing promised objects fail closed. Agents still operate with the permissions, sandbox, tools, and repository commands provided by their host and developer.

Security reports and automated reviews are evidence, not certification or deployment authorization.
