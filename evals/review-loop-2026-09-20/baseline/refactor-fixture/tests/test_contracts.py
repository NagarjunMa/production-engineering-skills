import unittest
from adapters import web_tag, cli_tag
from plugins import run_registered


class ContractTests(unittest.TestCase):
    def test_empty_adapters_remain_distinct(self):
        for value in ["", "   ", "\t\n"]:
            with self.subTest(value=value):
                self.assertEqual(web_tag(value), (422, {"error": {"message": "empty tag"}}))
                self.assertEqual(cli_tag(value), (2, "error: empty tag"))

    def test_dynamic_registration_success(self):
        self.assertEqual(run_registered(" HELLO "), "hello")

    def test_dynamic_registration_rejects_empty(self):
        with self.assertRaisesRegex(ValueError, "^empty tag$"):
            run_registered("  ")

    def test_unicode_and_whitespace_contracts(self):
        self.assertEqual(web_tag(" ÄB "), (200, {"tag": "äb"}))
        self.assertEqual(cli_tag(" ÄB "), (0, "äb"))
        self.assertEqual(run_registered(" ÄB "), "äb")
