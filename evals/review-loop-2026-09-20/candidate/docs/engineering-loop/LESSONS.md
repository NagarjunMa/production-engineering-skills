# Verified lessons

For isolated subprocess configuration, default-only tests miss dropped settings. This fixture passed two old tests while lower/higher non-default checks failed. Preserve env={} and send validated non-secret configuration explicitly through JSON. Detection: tests/test_worker_contract.py exercises limits below and above default plus independent credential isolation. Evidence: candidate-evidence/red.log and green.log. Applies to this JSON worker, not a general requirement to transport arbitrary environment settings.
