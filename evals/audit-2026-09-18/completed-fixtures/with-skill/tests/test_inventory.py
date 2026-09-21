import unittest
from stock import adjust_many, adjust_stock

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


class BatchStockTests(unittest.TestCase):
    def test_success_updates_only_touched_products(self):
        stock = {"A": 5, "B": 2, "C": 9}
        result = adjust_many(stock, [("A", 2), ("B", -2)])
        self.assertEqual(result, {"A": 7, "B": 0})
        self.assertEqual(stock, {"A": 7, "B": 0, "C": 9})

    def test_repeated_products_use_tentative_quantities(self):
        stock = {"A": 1, "B": 2, "C": 9}
        result = adjust_many(stock, [("A", 3), ("B", 0), ("A", -4), ("A", 2)])
        self.assertEqual(result, {"A": 2, "B": 2})
        self.assertEqual(stock, {"A": 2, "B": 2, "C": 9})

    def test_zero_delta_touches_zero_quantity_product(self):
        stock = {"A": 0, "B": 2}
        self.assertEqual(adjust_many(stock, [("A", 0)]), {"A": 0})
        self.assertEqual(stock, {"A": 0, "B": 2})

    def test_empty_batch_preserves_stock(self):
        for initial in [{}, {"A": 5, "B": 2}]:
            with self.subTest(initial=initial):
                stock = initial.copy()
                self.assertEqual(adjust_many(stock, []), {})
                self.assertEqual(stock, initial)

    def test_underflow_preserves_entire_stock(self):
        for adjustments in [
            [("A", -6)],
            [("B", 3), ("A", -6)],
            [("A", -3), ("A", -3), ("A", 10)],
        ]:
            with self.subTest(adjustments=adjustments):
                stock = {"A": 5, "B": 2}
                with self.assertRaisesRegex(ValueError, "^Negative stock$"):
                    adjust_many(stock, adjustments)
                self.assertEqual(stock, {"A": 5, "B": 2})

    def test_unknown_product_preserves_entire_stock(self):
        for initial, adjustments in [
            ({}, [("MISSING", 0)]),
            ({"A": 5, "B": 2}, [("MISSING", 1)]),
            ({"A": 5, "B": 2}, [("A", 2), ("B", -1), ("MISSING", -1)]),
        ]:
            with self.subTest(initial=initial, adjustments=adjustments):
                stock = initial.copy()
                with self.assertRaises(KeyError) as error:
                    adjust_many(stock, adjustments)
                self.assertEqual(error.exception.args, ("MISSING",))
                self.assertEqual(stock, initial)

    def test_first_invalid_pair_determines_error(self):
        for adjustments, error_type in [
            ([("B", 1), ("A", -6), ("MISSING", 1)], ValueError),
            ([("B", 1), ("MISSING", 1), ("A", -6)], KeyError),
        ]:
            with self.subTest(adjustments=adjustments):
                stock = {"A": 5, "B": 2}
                with self.assertRaises(error_type):
                    adjust_many(stock, adjustments)
                self.assertEqual(stock, {"A": 5, "B": 2})
