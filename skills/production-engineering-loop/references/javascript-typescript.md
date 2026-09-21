# JavaScript and TypeScript Guidance

Use repository-native scripts, package-manager locks, framework conventions, and CI configuration as the source of truth. The examples below are decision criteria, not commands to run blindly.

## Node and Package Management

- Use the locked package manager and supported runtime version.
- Prefer reproducible installs in CI and keep lockfile changes intentional.
- Review runtime and development dependency exposure separately; assess reachability before describing an advisory's application risk.
- Bound inputs, iteration, recursion, buffers, concurrency, retries, and response sizes on untrusted or high-volume paths.
- Check client lifetimes against the framework's execution model. Reuse connections where supported, without retaining request-specific credentials or tenant state across invocations.

## TypeScript and API Boundaries

- Keep strict type checking enabled and avoid assertions that bypass runtime uncertainty.
- Validate external input at the runtime boundary; static types do not validate JSON, headers, storage, environment variables, or extension messages.
- Preserve documented status codes, error shapes, field semantics, defaults, and version behavior for existing clients.
- Separate parsing and validation from business behavior and external-I/O adapters when that matches the repository architecture.

## React and Next.js

- Keep server-only code, secrets, privileged clients, and sensitive environment variables outside client bundles.
- Use Server Components by default when the repository does; introduce client boundaries only for browser state or interaction.
- Avoid sequential data-fetch waterfalls when requests are independent, but do not add caching without ownership, invalidation, and privacy rules.
- Test authorization in the server action or route handler, not only in middleware or the interface.
- Evaluate accessibility, loading, empty, error, retry, and reduced-motion states for changed interfaces.

## Browser Extensions

- Treat content scripts, extension pages, service workers, web applications, and backend APIs as separate trust boundaries.
- Validate every runtime message and web response; do not trust page DOM content.
- Keep permissions and host permissions minimal and review any increase explicitly.
- Assess manifest/package versioning when packaged files or permissions change.
- Preserve compatibility between older published extensions and newer backends, or version and communicate the break.
- Test service-worker suspension, missing listeners, stale authentication, restricted pages, and offline or timeout behavior when relevant.

## Tests and Evidence

- Use unit tests for pure rules and edge cases, integration tests for module boundaries, contract tests for independently deployed clients, and end-to-end tests for critical user paths.
- Mock external APIs in routine tests. Use an authorized sandbox for provider-specific behavior that cannot be represented faithfully by a mock.
- Prefer assertions on behavior and invariants over snapshots of generated prose or internal implementation details.
- Measure bundle, latency, memory, query count, or cost when the change can materially affect it. Explain missing measurements when they would affect the review decision.
