# Review handoff

- Contract: repository-relative path and complete requirements (include content if reviewer cannot access source).
- Repository/isolated copy location:
- Risk tier and reason:
- Target branch, base, merge base (verified or explicitly unknown):
- Snapshot manifest location and ID:
- Committed/dirty/untracked state; intentionally excluded unrelated work:
- Relevant source, callers, tests, configuration, architecture records:
- Acceptance criterion → expected behavior → selected check → plausible wrong implementation:
- Historical commands/results/logs with tested snapshots (not reviewer-verified):
- Required repository/hosted gates and current status:
- Boundary/privacy/compatibility concerns and unresolved assumptions:
- Reviewer policy: required context/model/human review; available host capability:
- Reviewer rounds used / maximum:
- Output report location (authorized scratch space or inline):

Use the bundled reviewer prompt. The receiver needs access to the actual source snapshot; hashes alone cannot reconstruct code. Verify the manifest before and after review. For compact work, these fields may be a short section in the existing feature record. Full work can link a separate packet; avoid copying entire project documentation.
