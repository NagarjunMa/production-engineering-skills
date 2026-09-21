# Persistent project learning

Use for substantive implementation, project onboarding, and explicitly requested codebase documentation. The purpose is to make later work better informed without making each task repeat the initial investigation.

## Where knowledge lives

First locate the repository's existing product brief, architecture guide, decisions, test plans, and feature records. Update or link those sources rather than creating a competing source of truth. If no equivalent exists, use this small default structure in the **target project**:

```text
docs/engineering-loop/
  PROJECT.md                  Current product and codebase map
  features/<feature-slug>.md   Contract, evaluations, file changes, and status
  LESSONS.md                  Only when a reusable, evidenced lesson exists
```

These files are ordinary project documentation. No database, background process, private memory service, or model training is required. Do not put project-specific knowledge into this installed skill. Documentation edits are part of substantive implementation unless the user's scope excludes them. For a read-only review or plan-only request, keep proposed records in the response unless documentation edits were explicitly requested. Do not change repository instruction files just to force adoption.

Use the bundled [project template](../assets/project-template.md), the selected [compact/full feature record](documentation-modes.md), and [lesson template](../assets/lesson-template.md) as starting structures. Fill only useful sections; remove empty scaffolding. Resolve these template paths relative to this skill, and output the filled documents in the target repository. Adapt to existing documentation conventions.

The full feature template retains the user's PRI-style contract and adds an Execution Context. Preserve explicitly supplied sections, marking inapplicable fields with a reason rather than deleting required context. Follow [task-context.md](task-context.md) in either mode to record verified/candidate/planned paths, symbols, callers, tests, progress, and freshness. Link the feature's detailed location map from the project summary rather than duplicating it there.

## Bootstrap from the problem and source

1. **Understand intent.** Read the problem statement, supplied specifications, and relevant prior decisions. Record the intended users, problem, workflows, success criteria, constraints, and non-goals. Cite a repository source or summarize the user's decision with its date. Label inference and unanswered questions; do not invent a product vision from dependencies.
2. **Inventory the repository.** Check instructions and worktree state, then inspect the owned file tree, manifests, lockfiles, entry points, tests, CI, schemas, and deployment definitions. Exclude vendor dependencies, build artifacts, binaries, and generated output from routine source reading; inspect generator sources when relevant. Do not collect secret values or private customer data into memory.
3. **Map responsibilities.** Record the observed language/runtime, framework, package manager, persistence, integrations, build/test tools, and deployment model. Distinguish declared version constraints from locked/resolved versions. Link evidence and note unknowns. Describe important directories, files, entry points, data flows, and trust boundaries. Group repetitive files by responsibility rather than dumping a giant tree.
4. **Map features and coverage.** Identify implemented, partial, planned, and unknown behavior from code and tests. Link feature records, relevant files, and existing checks. Record which modules were inspected deeply, which were inventoried only, and what remains unread. Sampling never establishes a complete audit.
5. **Establish the next task.** Select work from the current user request or accepted plan. Define its evaluation contract before changing behavior. A discovered gap becomes a candidate follow-up, not authorization to build it.

For an explicit whole-codebase read, enumerate in-scope first-party source and work through it in batches, maintaining a coverage ledger by directory or subsystem. If size, access, or time prevents complete inspection, preserve the remaining areas and next entry point and report partial coverage. For ordinary feature work, prioritize the affected subsystem after creating the high-level map.

For a greenfield project, the problem statement is the initial source. Record a proposed stack and planned file responsibilities separately from established decisions and actual files. Do not claim that a library, schema, feature, or evaluation exists until it does. Create the evaluation contract, build the smallest useful increment, then update the map from the resulting files.

## Resume without relearning everything

At the next substantive task, read the compact project summary, relevant feature record, and lessons whose applicability matches the change. Check current instructions, worktree state, recent changes, manifests, and relevant source before relying on them. Record a commit/revision when available and mark uncommitted work explicitly; without Git, use a dated source snapshot description.

Treat memory as a fallible index into evidence. If a path was renamed, a dependency changed, or a test result belongs to an older revision, refresh that fact. Keep historical results labeled with their tested revision; they are not a pass for today's code. When user intent and source conflict, state the discrepancy and resolve the necessary product decision rather than silently treating source as the specification.

Load detailed records on demand. Keep `PROJECT.md` a current summary, not a session transcript. Archive completed details through the project's normal documentation conventions, merge duplicate lessons, and supersede obsolete guidance with a reason. Preserve relevant user-authored text and concurrent edits.

## Close the learning loop

After implementation and evaluation, update only affected records:

- **Project map:** changes to actual stack, responsibility boundaries, feature index, and current inspection gaps.
- **Feature record:** acceptance criteria, files created/changed/renamed/removed and why, test locations, commands, results, tested revision, and outstanding issues. Derive the file list from the actual worktree/diff; do not attribute unrelated edits to this task.
- **Lessons:** a confirmed failure or useful correction, its cause and evidence, where it applies, the narrower decision for next time, and a regression check or manual detection procedure. Record unresolved explanations as hypotheses, not lessons established as fact.

An unsuccessful attempt can still improve the record: preserve the failing case, what was ruled out, and the next bounded hypothesis. Do not repeatedly retry it unchanged. A successful task need not invent a new lesson.

Learning has a concrete chain: **observed outcome → supported explanation → scoped lesson → improved evaluation → use on a later relevant task**. Changes to the reusable skill itself are separate, explicit maintenance work; project experience does not authorize silent self-modification, cross-project memory sharing, or weaker release gates.
