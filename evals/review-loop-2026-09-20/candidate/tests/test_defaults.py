import unittest
from parent import Tool


class DefaultTests(unittest.TestCase):
    def test_default_accepts(self):
        self.assertEqual(Tool().worker("hello")["value"], "HELLO")

    def test_default_rejects(self):
        self.assertEqual(Tool().worker("x" * 13)["error"], "text exceeds limit")
