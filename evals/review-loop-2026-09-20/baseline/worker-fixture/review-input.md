# Incoming review report
1. parent.py Tool.worker drops configured limits at the subprocess boundary. A limit of 5 accepts six characters in the worker while local rejects them. Correct the effective config transport without inheriting credentials.
2. adapters.py web_error and cli_error look redundant. Replace them with one shared error response shape for consistency.
3. legacy.py has the vague name thingy. Rename it while here.
