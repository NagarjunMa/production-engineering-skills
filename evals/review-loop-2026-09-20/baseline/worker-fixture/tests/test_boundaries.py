import os
import unittest
from unittest.mock import patch
from adapters import cli_error, web_error
from parent import Tool


class BoundaryTests(unittest.TestCase):
    def test_configured_boundaries(self):
        for limit, length, accepted in [(5, 5, True), (5, 6, False), (20, 13, True), (20, 20, True), (20, 21, False)]:
            with self.subTest(limit=limit, length=length):
                tool = Tool(limit)
                text = "x" * length
                if accepted:
                    self.assertEqual(tool.local(text), "X" * length)
                    self.assertEqual(tool.worker(text)["value"], "X" * length)
                else:
                    with self.assertRaisesRegex(ValueError, "text exceeds limit"):
                        tool.local(text)
                    self.assertEqual(tool.worker(text).get("error"), "text exceeds limit")

    def test_synthetic_credentials_stay_outside_worker(self):
        with patch.dict(os.environ, {"FIXTURE_API_TOKEN": "synthetic-not-a-secret", "TEXT_LIMIT": "999"}):
            response = Tool(5).worker("xxxxxx")
        self.assertNotIn("FIXTURE_API_TOKEN", response["environment_names"])
        self.assertNotIn("TEXT_LIMIT", response["environment_names"])
        self.assertEqual(response.get("error"), "text exceeds limit")

    def test_distinct_adapter_contracts(self):
        self.assertEqual(web_error("bad"), (400, {"error": {"message": "bad"}}))
        self.assertEqual(cli_error("bad"), (2, "error: bad"))
