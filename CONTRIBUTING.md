# Contributing

Improve decisions the agent makes, rather than adding a rule for every imaginable failure. Keep the workflow useful for both small fixes and substantial engineering work.

The canonical skill lives in `skills/production-engineering-loop/`. Keep references relative and bundled. Avoid required vendor tools, personal paths, model names, or delegation. `agents/openai.yaml` is optional host metadata; the workflow must work without it.

For a change, explain the observed problem, show a realistic task where the old guidance failed, and describe the new behavior. Preserve review-only mode, scope boundaries, honest validation reporting, and a finite stopping condition. Add conditional detail to a reference only when it earns its context cost.

Project memory belongs to the target repository and must remain evidence-backed, scoped, and refreshable. Keep templates portable and bundled. Evaluate stale memory, greenfield plans, and acceptance criteria derived independently of the implementation when changing the learning loop. Do not make a project lesson silently mutate the shared skill or create mandatory process for trivial edits.

Run the development commands in [README.md](README.md). For instruction changes, also run applicable [behavioral scenarios](evals/README.md) in disposable workspaces and report actual outcomes. A schema check or wording match cannot establish that an agent followed a workflow. Do not commit private code, secrets, or raw transcripts containing personal data.

Record compatibility claims separately from observed runs. Update installation sources when paths change. Keep both license copies identical so the installed package retains its license.
