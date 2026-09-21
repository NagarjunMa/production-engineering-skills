import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from adapters import cli_error, web_error
from parent import Tool


class WorkerContractTests(unittest.TestCase):
    def test_configured_boundaries(self):
        for limit in (1, 5, 12, 20):
            for length in (limit, limit + 1):
                with self.subTest(limit=limit, length=length):
                    text = "x" * length
                    tool = Tool(limit)
                    result = tool.worker(text)
                    if length > limit:
                        with self.assertRaisesRegex(ValueError, "text exceeds limit"):
                            tool.local(text)
                        self.assertEqual(result.get("error"), "text exceeds limit")
                    else:
                        self.assertEqual(tool.local(text), "X" * length)
                        self.assertEqual(result.get("value"), "X" * length)

    def test_python_characters_and_prestrip_limit(self):
        self.assertEqual(Tool(3).worker("é🙂x")["value"], "É🙂X")
        self.assertEqual(Tool(3).worker(" x ")["value"], "X")
        self.assertEqual(Tool(2).worker(" x ").get("error"), "text exceeds limit")

    def test_credential_isolation_and_launch_contract(self):
        sentinel = "PEL_SYNTHETIC_CREDENTIAL"
        with patch.dict(os.environ, {sentinel: "fake-only-test-value"}):
            with patch("parent.subprocess.run", wraps=subprocess.run) as run:
                result = Tool(20).worker("x" * 13)
            self.assertNotIn(sentinel, result["environment_names"])
            self.assertEqual(os.environ[sentinel], "fake-only-test-value")
            self.assertEqual(run.call_args.kwargs["env"], {})
            self.assertTrue(Path(run.call_args.args[0][0]).is_absolute())
            self.assertEqual(result.get("value"), "X" * 13)

    def test_invalid_parent_limits(self):
        for limit in (True, False, 0, -1, 1.5, "5", None):
            with self.subTest(limit=limit):
                with self.assertRaisesRegex(ValueError, "limit must be a positive integer"):
                    Tool(limit)

    def direct_worker(self, request):
        completed = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parents[1] / "worker.py")],
            input=json.dumps(request), text=True, capture_output=True,
            env={}, check=True, timeout=5,
        )
        return json.loads(completed.stdout)

    def test_invalid_receiver_limits(self):
        for limit in (True, False, 0, -1, 1.5, "5", None):
            with self.subTest(limit=limit):
                self.assertEqual(
                    self.direct_worker({"text": "x", "limit": limit}).get("error"),
                    "limit must be a positive integer",
                )

    def test_legacy_receiver_default(self):
        self.assertEqual(self.direct_worker({"text": "x" * 12})["value"], "X" * 12)
        self.assertEqual(self.direct_worker({"text": "x" * 13})["error"], "text exceeds limit")

    def test_distinct_adapter_contracts(self):
        self.assertEqual(web_error("bad"), (400, {"error": {"message": "bad"}}))
        self.assertEqual(cli_error("bad"), (2, "error: bad"))
