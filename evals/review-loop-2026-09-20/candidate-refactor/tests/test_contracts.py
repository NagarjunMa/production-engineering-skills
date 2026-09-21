import unittest
from adapters import cli_tag, web_tag
from helpers import normalize_tag
from plugins import run_registered


class ContractTests(unittest.TestCase):
    def test_success_contracts(self):
        for value, expected in ((" HELLO ", "hello"), ("  Straße ", "straße"), ("a b", "a b"), ("\tMiXeD\n", "mixed")):
            with self.subTest(value=value):
                self.assertEqual(normalize_tag(value), expected)
                self.assertEqual(run_registered(value), expected)
                self.assertEqual(web_tag(value), (200, {"tag": expected}))
                self.assertEqual(cli_tag(value), (0, expected))

    def test_empty_contracts(self):
        for value in ("", " ", "\t\n"):
            with self.subTest(value=value):
                for handler in (normalize_tag, run_registered):
                    with self.assertRaisesRegex(ValueError, "^empty tag$"):
                        handler(value)
                self.assertEqual(web_tag(value), (422, {"error": {"message": "empty tag"}}))
                self.assertEqual(cli_tag(value), (2, "error: empty tag"))
