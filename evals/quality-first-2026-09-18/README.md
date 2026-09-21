# Quality-first documentation modes — bounded forward evaluation

Date: 2026-09-18. Skill instructions: v0.4.0. These evaluations check concrete decisions and artifacts; they are not a cross-host benchmark or proof of superiority over a baseline.

## Compact implementation

A fresh independent agent received the [task](task.txt), a disposable copy of [starting-fixture](starting-fixture/README.md), and the revised skill with its resources. It did not receive evaluator expectations or the parent conversation. It was restricted to that project and skill: no network, installations, commits, deployment, additional agents, or parent-repository inspection.

The fixture is a small Python library. Its policy module owns subtotal validation and the fee rule. Web and CLI adapters intentionally expose different output/error contracts. The feature adds ordered batch web quotes with independent per-item failure handling. The experiment tests whether the agent preserves that ownership and the intentional differences while documenting the task proportionally.

Observed result:

- Chose Standard risk and compact documentation, with concrete design rationale and criterion-to-evidence mapping.
- Added one function in the existing web adapter, delegating to its existing single-item operation. No copied fee policy, new dependency, generic framework, or extra layer.
- Preserved the policy module and CLI source unchanged, with compatibility coverage for both adapters.
- Added failure, threshold, ordering, empty-input, and input-preservation tests.
- Created a current project summary and a compact feature record; did not generate the full PRI template.

The agent reported a three-test baseline and an intended behavioral red state using a minimal scaffold. The parent reviewed the completed code, tests, and documentation, and independently executed the nine-test final suite. Intermediate red-state evidence is agent-reported rather than independently replayed.

The parent also prepared [verify_quotes.py](verify_quotes.py) before inspecting the implementation. Both the 1,111 bounded batch cases and 20 existing-entrypoint cases passed. A negative control that dropped invalid entries was rejected. These are combinations over one small domain, not independent feature-building trials. Architecture fit was assessed separately by source/caller inspection, not inferred from the test count.

Retained evidence:

- [Starting source](starting-fixture/README.md), [completed source](completed-fixture/README.md), and [diff](compact.diff).
- [Compact feature record](completed-fixture/docs/engineering-loop/features/web-quotes.md).
- [Actual parent-run results and artifact hashes](results.json).
- [Tested skill file hashes](tested-skill-sha256.json). The test copy has the revised v0.4.0 behavior instructions; its UI metadata predates the final quality-focused wording. The skill was explicitly invoked, so native discovery/UI prompt behavior was not tested.

Run from the main repository root, using Python 3.11 and without `-O`:

```sh
python3 -B evals/quality-first-2026-09-18/verify_quotes.py evals/quality-first-2026-09-18/completed-fixture
```

From the completed fixture directory:

```sh
python3 -B -m unittest discover -s tests -v
```

The evaluator imports supplied Python code; use it only with trusted fixtures. Source artifacts permit deterministic acceptance rechecking. Exact model and host-version metadata were unavailable, and a new agent run need not reproduce identical output. This run had no no-skill comparison, so it establishes bounded instruction-following behavior, not causal quality improvement.

## Full planning

A second scenario uses the completed library in a separate disposable directory plus a [supplied full PRI contract](full-supplied-contract.md). The [request](full-task.txt) authorizes editing only that plan for a new additive currency-aware API. It prohibits implementation and other file edits. The same agent continues for this scenario; this is not a second independent fresh-session test.

The parent reviewed the [completed full plan](full-completed-plan.md) and [diff](full.diff). All 29 supplied headings remained in order and five checked requirement lines, including the compatibility invariant, remained unchanged. The plan identifies canonical rule ownership, a single additive adapter, observable error semantics labeled as proposals, criterion-to-check mapping, and rollback considerations. It selects Significant risk and full documentation.

The parent independently compared bytes and confirmed all eight other files were unchanged. The API is unimplemented, all acceptance boxes remain unchecked, and status is Planned. The agent reported a fresh nine-test baseline pass; the parent did not repeat those unchanged runtime tests, having verified that implementation/tests match the independently tested compact output. Structural outcomes and the final plan hash are recorded in results.json. Links/paths inside the archived plan refer to its original project location; restore it as `docs/engineering-loop/features/currency-quotes.md` alongside the completed fixture to recreate that layout.

## Remaining coverage

Greenfield architecture selection, defective local patterns, risk escalation, concurrency, databases, migrations, and real host activation still need separate behavioral evaluation. Compact and full modes share applicable quality obligations by instruction; no experiment establishes universal adherence. There is no token-saving measurement or performance claim here.
