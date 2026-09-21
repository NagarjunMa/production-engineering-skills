# Code Quality Review and Cleanup

Use during implementation and for standalone reviews of existing code, regardless of who wrote it. Evaluate concrete behavior and maintenance costs; suspected AI authorship is not evidence of a defect.

## Establish the Local Design Baseline

Read architecture decisions, applicable repository instructions, lint/type configuration, and representative neighboring implementations. Trace the affected entry points, callers, shared helpers, and external boundaries. Identify which patterns actually govern the changed responsibility, such as validation, state ownership, persistence, error handling, or dependency injection.

Compare against maintained examples and documented decisions rather than copying the nearest file blindly. If conventions conflict, explain the evidence for the chosen approach. Preserve a local convention unless it causes an evidenced defect, violates an applicable requirement, or materially obstructs the requested change.

Use language and framework idioms appropriate to the repository's installed versions. Consult authoritative primary sources, with version and access date, when a recommendation depends on current guidance. Label each basis as a mandatory requirement, documented repository convention, or engineering recommendation. A fashionable or newly published pattern is not automatically the right replacement.

## Establish a Design When One Is Missing

Before adding files to a greenfield project or an inconsistent subsystem, outline the smallest design that explains the current use case:

- Which module owns each business rule and state transition; which entry point orchestrates the operation.
- Inputs, outputs, errors, invariants, and ownership of mutable state at the affected interfaces.
- Where external I/O enters and which dependencies point toward which modules. Keep domain rules independently testable when that boundary is meaningful.
- Which existing rule or component can be reused, what must remain separate, and why.
- How to verify the behavior through real consumers and relevant boundaries.

A few functions in one cohesive module may satisfy this design. Add an adapter, service, repository, strategy, or other pattern only when its responsibility solves an observed problem such as isolating I/O or supporting actual alternative behavior. Do not create directories, interfaces, classes, or layers solely to resemble a reference architecture. Small projects need sound boundaries, not production-scale infrastructure.

Put a short design basis in the feature record, or link an existing architecture decision. Use the compact or full documentation mode already selected. Explain a substantial new boundary or deviation with the problem, chosen approach, simpler alternative, and tradeoff; do not require a separate ADR for every helper. If the existing pattern is defective, demonstrate the problem, choose a sound in-scope alternative, and identify wider migration work without silently rewriting the repository.

## Define the Applicable Quality Bar

Establish design constraints before implementing, then inspect them against the result. Examples include reusing a verified pricing policy, keeping request parsing out of domain validation, preserving dependency direction, or keeping an atomic operation free of partial writes. Name the relevant files/symbols and consumers; avoid slogans such as "SOLID-compliant" without a concrete decision.

Use the repository's maintained formatter, linter, type checks, architecture/dependency rules, tests, and CI gates where applicable. Connect security, accessibility, protocol, or language guidance to the actual changed boundary. Verify version-sensitive recommendations against primary sources. When sources or tools are unavailable, identify the specific uncertainty. Do not introduce a framework, scanner, dependency, or certification exercise merely because the user asks for industry standards.

Quality is assessed through observable correctness and supported maintenance decisions. Compact documentation, an early-stage project, a desire to ship quickly, or a passing happy-path test does not waive relevant checks. Conversely, a named pattern, zero duplicated lines, or more modules does not establish quality.

## Inspect the Implementation

Apply the relevant checks, using concrete examples from the reviewed code:

| Area | What to examine | Decision rule |
| --- | --- | --- |
| Pattern fit | Responsibility placement, dependency direction, data flow, lifecycle, and consistency with comparable maintained code | Prefer the existing sound approach; justify deviations with the problem they solve. Avoid imposing a named pattern merely for uniformity. |
| Redundancy | Repeated business rules, validation, mappings, queries, state, branches, and wrappers | Search for semantic duplicates as well as copied text. Consolidate rules that must evolve together; preserve intentional differences and independent boundaries. |
| Modularity | Mixed responsibilities, circular dependencies, hidden state, oversized public interfaces, and functions doing unrelated work | Split at a meaningful responsibility or lifecycle boundary. Prefer explicit dependencies and cohesive modules; line-count thresholds alone do not justify a split. |
| Abstractions | One-use forwarding layers, generic frameworks for a single case, boolean-driven modes, and premature extension points | Simplify when indirection obscures behavior without serving a current requirement. Keep adapters or interfaces that protect an actual boundary even with one implementation. |
| Readability | Domain names, units, control flow, nesting, mutation, error semantics, and type precision | Make intent and ownership clear. Prefer a straightforward implementation over clever compression; avoid repository-wide cosmetic renaming. |
| Comments and documentation | Module responsibilities, public contracts, surprising invariants, workarounds, and stale explanations | Explain why, constraints, and non-obvious decisions. Let clear names and structure explain routine mechanics; comments cannot substitute for modularity. |
| Incomplete or misleading code | Placeholder success paths, swallowed exceptions, fabricated defaults, disconnected helpers, debug output, obsolete TODOs, and unjustified lint/type suppressions | Trace execution and consumers before declaring code broken or dead. Replace incomplete behavior only when the intended contract is known. |
| Logic gaps | Missing negative paths, validation or permission bypasses, stale state, races, resource cleanup, and partial failure | Demonstrate a reachable failure condition and affected invariant. Use the main skill's risk tier and broader review dimensions for the resulting finding. |

Do not infer dead code from a text search alone: inspect exports, dynamic registration, reflection, framework conventions, generated inputs, and external consumers where relevant. Edit generator sources rather than disposable output. Leave vendor code outside routine cleanup.

## Decide Whether Duplication Should Be Removed

Before extracting or reusing a helper:

1. Identify the duplicated responsibility and all relevant occurrences within scope, including existing canonical implementations.
2. Compare semantics: defaults, error behavior, side effects, ordering, authorization, caching, and lifecycle. Similar syntax can implement different contracts.
3. Determine whether the occurrences share ownership and must change together. Reuse a canonical rule when appropriate; avoid coupling independently evolving modules, clients, or trust boundaries solely to reduce repetition.
4. Choose the smallest change that reduces drift or maintenance cost. A clear shared function may suffice; a new framework rarely does.
5. Verify affected callers and differences that must remain. Preserve independent test expectations instead of importing the production rule into the expected result.

Intentional repetition may remain when extraction would increase coupling or obscure distinct behavior. Explain significant decisions to retain it. Avoid arbitrary duplication quotas or targeting a minimum number of lines removed.

## Make Comments Useful

Add or update comments when a reader needs context the code cannot convey clearly: a module's non-obvious responsibility, a public API's invariants, dependency restrictions, concurrency assumptions, or the reason for a workaround. Follow the repository's documentation format; include a relevant issue or source when it explains a temporary constraint.

Remove misleading, stale, or line-by-line narration. Keep contractual documentation and rationale that still matter. Do not enforce a comment on every function, repeat types in prose, or use long comments to excuse tangled code. Check comments against the final implementation after refactoring.

## Turn Observations Into Actionable Findings

For each actionable issue, record:

- severity and confidence, with a file and narrow line location;
- the failure scenario or concrete maintenance cost, supported by callers, tests, or other evidence;
- the applicable requirement, convention, or recommendation;
- the smallest corrective action and evidence needed to validate it;
- whether it was introduced by the current work or already existed, and its final status.

Prioritize exploitable or data-loss defects, then behavior and reliability failures, then concrete maintenance improvements. Keep optional style preferences separate and non-blocking. Avoid invented quality scores, unsupported claims of industry compliance, and findings based solely on personal taste. A passing linter is useful evidence but does not establish sound architecture or behavior.

## Fix and Verify Within Scope

When fixes are authorized, resolve relevant findings as part of implementation or cleanup. Establish the pre-change state, preserve unrelated edits, and separate behavior-preserving cleanup from intentional bug fixes so their effects can be assessed. For uncertain behavior with material regression risk, add focused characterization coverage before refactoring; if the intended behavior is unknown, record the uncertainty instead of silently redefining it.

Use repository-native formatting, linting, type checks, tests, and required gates as applicable. Existing duplication or complexity tools can help locate candidates, but inspect their results before changing code. Do not introduce a new dependency or mandatory gate merely to produce a quality metric.

After a correction, review the actual diff and affected consumers, and rerun relevant checks. Track pre-existing failures separately. If a fix requires a broader redesign or changes an unclear public contract, finish safe in-scope work and report the remaining decision. Stop when supported in-scope findings are resolved and validated, or a concrete blocker is recorded; do not keep refactoring to chase aesthetic perfection.

At handoff, give concise evidence for the material design choices: the pattern/canonical rule used, boundaries and consumers inspected, duplication retained or removed and why, and checks that protect the behavior. Report unknown coverage and unresolved findings. Do not claim to have eliminated all redundancy or reviewed the entire codebase from a local feature inspection.
