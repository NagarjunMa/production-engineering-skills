# Project
Disposable Python text-normalization tool for local and subprocess execution. Source: README and evaluation task, 2026-09-20. No dependencies, CI, deployed systems, or credentials.

Inspected all first-party source and tests at initial HEAD (see logs). `policy.py` owns normalization and default length; `parent.py` configures tools and owns subprocess orchestration; `worker.py` is a JSON adapter; `adapters.py` intentionally contains independent web/CLI presentation contracts. `legacy.py` is unrelated.

Run `python3 -m unittest discover -s tests -v`. Feature: [worker config](features/worker-config.md). No externally deployed consumers were available to inspect.
