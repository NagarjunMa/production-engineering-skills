# Feature evaluations before implementation

Use when adding a feature or making a meaningful behavior change. An evaluation establishes whether a user-relevant requirement is met. It may be a unit, integration, contract, end-to-end, accessibility, performance, or manual check; use the smallest credible method for the risk.

## Build an evaluation contract

Before changing behavior, write the goal and numbered acceptance criteria in the existing feature record or selected [compact/full record](documentation-modes.md). Small related fixes can extend an existing record. Both formats retain the same applicable evaluation obligations. For each criterion identify:

| Field | What to establish |
| --- | --- |
| Criterion | Observable outcome and the requirement or user decision supporting it |
| Case | Representative input, preconditions, relevant data/state, and action |
| Expected result | Output, state transition, side effects, and effects that must not occur |
| Method | Existing or planned test location and command, or exact manual procedure |
| Coverage | Happy path and material boundary, negative, compatibility, or recovery cases |
| Wrong implementation | Plausible mistake for each material criterion and the selected check that rejects it |
| Result | Not run, passed, failed, or blocked; dated evidence and tested revision |

Keep **planned evaluations** separate from checks that already exist and results from checks actually executed. If intended behavior is ambiguous, record the question before selecting an expected outcome. Do not infer the desired result from a snapshot of the current implementation.

Include material design constraints alongside behavioral criteria: a shared rule's canonical owner, a protected dependency boundary, or an intentional difference between consumers. Check these using source/caller review and existing architecture checks where available. Do not force subjective design judgments into brittle tests that assert folder names or helper calls. Passing behavioral tests and a justified design review provide different evidence; retain both where relevant.

Follow the feature contract's regression-first sequence when executable testing is meaningful: establish the baseline, add/update the behavioral case, observe the intended failure, implement, and refactor with tests green. For new features, create the minimal runnable scaffold if needed before establishing the behavioral failure; a missing import or broken environment alone is not the intended red state. For refactors, establish passing characterization coverage for behavior that must remain unchanged, including intentional differences between similar modules. Record a TDD exception when executable testing is not meaningful and identify structural or repository-native evidence instead. When tests are meaningful but unavailable, record a blocker and incomplete validation rather than an exception or a fabricated pass.

## Select evidence that can catch a mistake

- Prefer real boundary or integration coverage where mocks would conceal the defect. Use local fakes or an authorized sandbox for external services; record what mocks cannot verify.
- For execution or serialization boundaries use [execution-boundaries.md](execution-boundaries.md): non-default configuration, credential isolation, and receiver behavior must survive real transport.
- When useful, prove a targeted mutation or negative control fails the selected check for the intended reason. Mutate only disposable copies. Missing imports, setup failures, or tests repeating the implementation do not establish defect detection.
- Derive expected values independently of the production helper being tested. Check meaningful properties and state transitions, not only internal calls or self-generated snapshots.
- Include forbidden side effects for authorization, transactions, billing, retries, and deletion. A denied request must not still write data; a retry must not duplicate the effect.
- For interfaces, cover relevant keyboard/accessibility and loading/error/recovery behavior, not only screenshots. For performance, specify workload, environment, and a justified target before measuring.
- For probabilistic or AI features, keep representative evaluation data distinct from development examples, define a human-reviewable rubric and material failure thresholds, and repeat runs where variation matters. Do not present an LLM's self-score as ground truth or silently tune against a held-out set.
- Reuse the repository's tooling. Introduce a new framework or service only when the task needs it, not merely to make a dashboard or quality score.

## Use outcomes to improve the next iteration

Run the relevant checks against the actual changed code and record commands, results, environment limits, and revision. Passing selected tests does not establish full coverage. Missing dependencies or credentials mean blocked validation, not a simulated pass.

Name the validation mode: behavioral change (intended red/green), pure refactor (passing characterization before/after), or non-executable (justified structural/native checks). Mixed refactor/bug-fix tasks need distinguishable evidence for both. Use [review-evidence.md](review-evidence.md) for freshness and [independent-review.md](independent-review.md) for required review and supplied reports.

When a check fails, determine whether the implementation, environment, test, or requirement is at fault. Fix evidenced implementation defects within scope; change an expectation only when the agreed contract changed or evidence establishes that the test was wrong. Preserve a concise rationale. Keep pre-existing failures distinct.

When a defect escaped the original evaluation, add its reproducer or a check for the missing invariant where practical. Update the feature record and capture a scoped lesson only when supported. Do not grow an exhaustive test matrix for hypothetical failures. Stop when the contract and applicable checks pass or a concrete unresolved blocker is documented.
