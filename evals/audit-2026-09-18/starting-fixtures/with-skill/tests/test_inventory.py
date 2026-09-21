import unittest
from stock import adjust_stock

class StockTests(unittest.TestCase):
    def test_increase(self):
        stock = {"A": 5, "B": 2}
        self.assertEqual(adjust_stock(stock, "A", 2), 7)
        self.assertEqual(stock, {"A": 7, "B": 2})

    def test_success_boundaries(self):
        for initial, delta, expected in [(5, -2, 3), (5, -5, 0), (5, 0, 5), (0, 0, 0), (0, 2, 2)]:
            with self.subTest(initial=initial, delta=delta):
                stock = {"A": initial, "B": 2}
                self.assertEqual(adjust_stock(stock, "A", delta), expected)
                self.assertEqual(stock, {"A": expected, "B": 2})

    def test_underflow_preserves_entire_stock(self):
        for initial, delta in [(5, -6), (0, -1)]:
            with self.subTest(initial=initial, delta=delta):
                stock = {"A": initial, "B": 2}
                before = stock.copy()
                with self.assertRaises(ValueError):
                    adjust_stock(stock, "A", delta)
                self.assertEqual(stock, before)

    def test_unknown_code_preserves_entire_stock(self):
        for initial in [{"A": 5, "B": 2}, {}]:
            for delta in [-1, 0, 1]:
                with self.subTest(initial=initial, delta=delta):
                    stock = initial.copy()
                    before = stock.copy()
                    with self.assertRaises(KeyError):
                        adjust_stock(stock, "MISSING", delta)
                    self.assertEqual(stock, before)
