import json
from pathlib import Path
import subprocess
import sys
from policy import DEFAULT_LIMIT, normalize_text, validate_limit


class Tool:
    def __init__(self, limit=DEFAULT_LIMIT):
        self.limit = validate_limit(limit)

    def local(self, text):
        return normalize_text(text, self.limit)

    def worker(self, text):
        completed = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("worker.py"))],
            input=json.dumps({"text": text, "limit": self.limit}), text=True, capture_output=True,
            env={}, check=True, timeout=5,
        )
        return json.loads(completed.stdout)
