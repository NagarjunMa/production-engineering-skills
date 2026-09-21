# Controlled audit pilot — 2026-09-18

This is one paired behavioral pilot of production-engineering-loop v0.3.0, not a token benchmark or a claim of statistically established improvement. The task, starting fixtures, completed artifacts, independent evaluator, differences, and command results are retained here.

## Question and setup

Can a fresh agent use repository memory, recover from a stale file map, and implement the next feature? Does a capable agent without the skill also satisfy the same behavior contract?

Both conditions started with the same small Python inventory implementation, four tests, and README. The source was renamed from `inventory.py` to `stock.py`, and the test import was updated. In the skill condition, the previous session's project and feature documents were retained with their old paths. In the baseline, those memory documents were omitted. The exact shared feature request is in [task.txt](task.txt).

Each condition used a separate fresh subagent with no inherited conversation. The skill condition explicitly invoked the installed skill; the baseline received the task without the skill or saved project memory. Both were bounded to their fixture and the shared task: no network, dependency installation, services, commits, deployment, or additional agents. The baseline was directed to implement and test without adding planning documents. This paragraph records the protocol; exact agent-wrapper transcripts were not exported.

Before the skill run, the parent installed the package locally using Skills CLI 1.7.0 with `--skill production-engineering-loop --agent codex claude-code cursor github-copilot gemini-cli --copy --yes`. The source argument was the local repository. All 13 package files matched the source in both `.agents/skills/production-engineering-loop` and `.claude/skills/production-engineering-loop`. This verifies local installer copying, not discovery, activation, or behavior inside five different host applications. Installed copies and Git metadata are excluded from the retained fixtures.

## Independent verification

The parent prepared [verify_stock.py](verify_stock.py) before receiving the implementations. It interprets the task contract separately from either implementation and checks 7,380 bounded batch cases plus 42 single-item regression cases. Cases cover repeated products, first-error order, intermediate underflow, unknown products, atomicity, untouched products, return values, and input-list preservation. This is exhaustive only over its small enumerated domain; it is not exhaustive over Python inputs or production behavior.

Both implementations passed all 7,422 cases and their own 11-test suites. The checker also rejected an intentionally broken implementation that mutated stock before the entire batch validated. See [results.json](results.json) for actual parent-run command results and completed-file hashes.

The skill run refreshed the stale map and carried the prior validate-before-write lesson into batch atomicity. Its saved project and feature records show this. Its historical red-test run is agent-reported evidence; the parent independently reran the completed suites and acceptance evaluator, not that intermediate scaffold.

## Reproduce acceptance checks

From the repository root, using Python 3.11:

```sh
python3 -B evals/audit-2026-09-18/verify_stock.py evals/audit-2026-09-18/completed-fixtures/with-skill
python3 -B evals/audit-2026-09-18/verify_stock.py evals/audit-2026-09-18/completed-fixtures/baseline
```

From each completed fixture directory:

```sh
python3 -B -m unittest discover -s tests -v
```

Do not run the evaluator with Python's `-O` option: it uses assertions. It imports and executes the supplied module, so use only trusted fixture inputs.

To run a new agent experiment, copy each starting fixture into a separate disposable directory, provide `task.txt`, and install/invoke the skill only for the skill condition. Fresh agent runs may produce different artifacts. The exact model version and token telemetry were unavailable and are recorded as null. This bundle reproduces acceptance verification of the retained outputs, not a deterministic reproduction of the original agent behavior.

## Interpretation and limitations

- Both conditions met the bounded behavior contract. This pilot does not establish a correctness advantage.
- Fresh-session memory reuse and stale-path recovery were observed once. This is evidence of feasibility, not general reliability.
- The treatment combines the skill and saved memory. It does not isolate their separate effects; a future comparison needs a third condition with the same memory but no skill.
- No model input/output tokens, cache effects, full tool-read trace, comparable wall-clock time, or human-review time were measured. File sizes and documentation length are context-cost proxies, not token savings.
- The baseline's absence of new planning documents was part of its assignment. Documentation differences cannot independently prove inefficiency, although they expose the workflow's storage/context costs.
- All scenarios use one tiny Python module. There is no evidence here for authentication, databases, migrations, deployment, UI accessibility, concurrency, or a real multi-package codebase.
- The reviewed repository had no commit. [reviewed-source-sha256.json](reviewed-source-sha256.json) fingerprints pre-audit source files but does not archive their contents. Archive or commit that source snapshot before publishing a fully reproducible release evaluation.

The retained fixture Markdown is historical evaluation output, not a current instruction or claim about the main repository. Original path references and historical status are preserved for inspection.
