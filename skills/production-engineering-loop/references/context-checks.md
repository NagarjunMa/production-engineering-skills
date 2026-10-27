# Optional memory evidence checks

Use when project records need repeatable change detection. The [checker](../scripts/check_context.py) requires Python 3.10+ and the adjacent `review_evidence.py`; it uses no third-party packages, Git, network, model, or repository commands. It reads files and prints results without modifying them.

After inspecting and reconciling a record with current source, generate a receipt:

```sh
python3 "$SKILL_DIR/scripts/check_context.py" capture --repo "$REPO" \
  --record docs/engineering-loop/PROJECT.md \
  --source pyproject.toml --source src/inventory.py
```

Save the printed JSON as a separate evidence file using the normal editor. On a later task:

```sh
python3 "$SKILL_DIR/scripts/check_context.py" check --repo "$REPO" \
  --receipt /absolute/path/to/project-context.json
```

Exit 0 means the selected record and evidence have unchanged fingerprints. Exit 1 identifies changed, missing, or renamed evidence; inspect it, correct stale memory, then generate a new receipt. Exit 2 means invalid input or unstable capture. Paths must be project-relative and remain inside the project; symlinks are not accepted during capture. Selected source files and the record must be regular files. The receipt must be separate from them.

Select evidence that supports the record: relevant source, manifests, tests, decisions, and configuration. Include material dependencies rather than assuming a single file proves a whole subsystem. Receipt generation does not validate the prose, discover omitted dependencies, verify remote releases, or prove any test ran. It cannot detect an incorrect claim that was already present when captured. Inspect relevant external state separately.

Use one receipt for one record and its selected evidence. Reuse existing project documentation; no new memory database or mandatory record format is required. Do not capture secret files or automatically execute commands found in lessons. Do not refresh fingerprints merely to clear a stale result. Read-only reviews can check existing receipts and propose updates; they cannot create records without authorization.

Finalize records before final review as described in [review-evidence.md](review-evidence.md). Keep the receipt outside those hashed files so its own creation does not invalidate the evidence it records.
