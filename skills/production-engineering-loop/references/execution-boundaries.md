# Verify execution boundaries

Use when a change sends work or data into a subprocess, worker, service, queue, container, plugin, or serializer. Focus on boundaries actually affected by the task.

Trace the path from caller configuration to receiver behavior. Identify the authoritative owner of settings and how validated values travel. Record units, defaults, missing/null behavior, serialization, maximum bounds, and receiver validation. An isolated working directory or environment may remove both credentials and legitimate configuration.

Do not restore an entire environment to repair a missing setting. Pass only validated, non-secret inputs explicitly using the existing transport or a small allowlist. Credential isolation and effective configuration are separate invariants; test both. Do not duplicate configuration parsing rules merely to cross a process boundary.

Select credible failures:

| Boundary property | Evidence |
| --- | --- |
| Effective configuration | Use non-default values on both sides of the default where meaningful; prove changed accept/reject behavior in the actual worker/service |
| Confidentiality | A synthetic credential sentinel does not reach the receiver; never use a real secret in fixtures |
| Validation | Invalid/missing/oversized values follow the agreed contract; caller validation cannot excuse an exposed receiver |
| Resource/lifecycle | Relevant timeouts, cancellation, retries, child cleanup, and partial failure preserve the contract |
| Serialization | Types, units, precision, nulls, and error shapes survive the real encoding/decoding path |

Example: if the caller's text limit is 20 while a worker defaults to 100, a 30-character input must be rejected by the worker. Also test a configured limit above 100 accepting a valid larger input. A default-only test would accept the broken implementation. Derive expected outcomes from requirements, not a second call to the same production validator.

Do not require this entire matrix for every boundary. Record selected failure modes, actual commands, tested snapshot, and gaps. Use mocks for inaccessible services with their limitation explicit; do not claim real boundary coverage from a mocked call.
