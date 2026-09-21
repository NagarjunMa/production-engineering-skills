# Bounded text worker project

Intent: README.md requires matching local/subprocess positive integer limits, Python-character counting, an explicitly empty child environment, and distinct web/CLI errors. No deployment is in scope.

Stack: dependency-free Python; observed runtime 3.11.1. No declared Python version, package configuration, CI, persistence or external services.

Inspected all first-party files at initial base ea6e6faa98e1e02d4b8e255b5d4a4f05e92118a1: parent.py orchestrates Tool and subprocess JSON; policy.py owns text normalization; worker.py decodes requests and produces value/error plus environment names; adapters.py owns independent transport error shapes; legacy.py is unrelated cosmetic data; tests/test_defaults.py covers defaults. README.md, AGENTS.md and review-input.md govern scope.

Feature: [worker configuration](features/worker-configuration.md). Native gate: `python3 -m unittest discover -s tests -v`. Source, tests, requirements and report were read, not merely inventoried. No external/deployment verification claimed.
