import unittest
from parcel.web import web_quote
from parcel.cli import cli_quote


class ExistingQuotes(unittest.TestCase):
    def test_web(self):
        self.assertEqual(web_quote(100), {"status": 200, "fee_cents": 499})

    def test_cli(self):
        self.assertEqual(cli_quote(5000), "Shipping: 0 cents")

    def test_errors(self):
        self.assertEqual(web_quote(-1), {"status": 400, "error": "invalid subtotal"})
        self.assertEqual(cli_quote(-1), "Error: invalid subtotal")
