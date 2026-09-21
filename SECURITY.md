# Security policy

## Supported version

Security fixes are applied to the latest published release. Until the first public release exists, the local `0.5.x` package is pre-release software and no hosted support channel is active.

## Reporting a vulnerability

After this repository is published, enable GitHub private vulnerability reporting and use that private channel for suspected vulnerabilities. Do not include real credentials, private customer data, or exploit activity against systems you do not own. A minimal synthetic reproduction, affected version, impact, and suggested boundary are useful.

Do not open a public issue for an unpatched vulnerability. If private reporting is not enabled on the future repository, the maintainer must add a verified private contact before describing a public security-reporting process; this document does not invent one.

## Security boundary

Installing the skill loads instructions and bundled resources; it has no installation hook, background service, required network connection, API key, or MCP server. The optional `review_evidence.py` helper uses local Python and Git when invoked. Its Git subprocesses are forced offline and missing promised objects fail closed. Agents still operate with the permissions, sandbox, tools, and repository commands provided by their host and developer.

Security reports and automated reviews are evidence, not certification or deployment authorization.
