import unittest
from copy import deepcopy
from parcel.web import web_quote, web_quotes
from parcel.cli import cli_quote


class ExistingQuotes(unittest.TestCase):
    def test_web(self):
        self.assertEqual(web_quote(100), {"status": 200, "fee_cents": 499})

    def test_cli(self):
        self.assertEqual(cli_quote(5000), "Shipping: 0 cents")

    def test_errors(self):
        self.assertEqual(web_quote(-1), {"status": 400, "error": "invalid subtotal"})
        self.assertEqual(cli_quote(-1), "Error: invalid subtotal")

    def test_policy_boundaries(self):
        for subtotal, fee in [(0, 499), (4999, 499), (5000, 0), (5001, 0)]:
            with self.subTest(subtotal=subtotal):
                self.assertEqual(web_quote(subtotal), {"status": 200, "fee_cents": fee})
                self.assertEqual(cli_quote(subtotal), f"Shipping: {fee} cents")

    def test_invalid_types(self):
        for subtotal in [True, False, 100.0, "100", None, [], {}]:
            with self.subTest(subtotal=subtotal):
                self.assertEqual(web_quote(subtotal), {"status": 400, "error": "invalid subtotal"})
                self.assertEqual(cli_quote(subtotal), "Error: invalid subtotal")


class BatchQuotes(unittest.TestCase):
    def test_order_and_boundaries(self):
        self.assertEqual(web_quotes([5000, 0, 4999, 5001]), [
            {"status": 200, "fee_cents": 0},
            {"status": 200, "fee_cents": 499},
            {"status": 200, "fee_cents": 499},
            {"status": 200, "fee_cents": 0},
        ])

    def test_invalid_items_do_not_stop_later_quotes(self):
        for invalid in [-1, True, False, 100.0, "100", None, [], {}]:
            with self.subTest(invalid=invalid):
                self.assertEqual(web_quotes([0, invalid, 5000]), [
                    {"status": 200, "fee_cents": 499},
                    {"status": 400, "error": "invalid subtotal"},
                    {"status": 200, "fee_cents": 0},
                ])

    def test_empty(self):
        self.assertEqual(web_quotes([]), [])

    def test_input_is_not_mutated(self):
        subtotals = [5000, {"subtotal": [100]}, [0], -1, 4999]
        original = deepcopy(subtotals)
        web_quotes(subtotals)
        self.assertEqual(subtotals, original)
