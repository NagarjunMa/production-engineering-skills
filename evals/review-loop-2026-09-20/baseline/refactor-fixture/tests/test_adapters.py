import unittest
from adapters import web_tag, cli_tag


class ExistingTests(unittest.TestCase):
    def test_web(self):
        self.assertEqual(web_tag(" HELLO "), (200, {"tag": "hello"}))

    def test_cli(self):
        self.assertEqual(cli_tag(" HELLO "), (0, "hello"))
