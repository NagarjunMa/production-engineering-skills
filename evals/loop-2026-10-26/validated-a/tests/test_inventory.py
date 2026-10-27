import unittest

from inventory import adjust_stock


class StockTests(unittest.TestCase):
    def test_adjustments_store_and_return_result_preserving_other_products(self):
        for starting, delta, expected in (
            (5, 2, 7),
            (5, 0, 5),
            (5, -2, 3),
            (5, -5, 0),
            (0, 2, 2),
            (0, 0, 0),
        ):
            with self.subTest(starting=starting, delta=delta):
                stock = {'A': starting, 'B': 9}
                self.assertEqual(adjust_stock(stock, 'A', delta), expected)
                self.assertEqual(stock, {'A': expected, 'B': 9})

    def test_negative_result_leaves_entire_dictionary_unchanged(self):
        for starting, delta in ((5, -6), (0, -1)):
            with self.subTest(starting=starting, delta=delta):
                stock = {'A': starting, 'B': 9}
                before = stock.copy()
                with self.assertRaises(ValueError):
                    adjust_stock(stock, 'A', delta)
                self.assertEqual(stock, before)

    def test_unknown_product_leaves_entire_dictionary_unchanged(self):
        for stock in ({'A': 5, 'B': 9}, {}):
            for delta in (-1, 0, 2):
                with self.subTest(stock=stock, delta=delta):
                    before = stock.copy()
                    with self.assertRaises(KeyError):
                        adjust_stock(stock, 'missing', delta)
                    self.assertEqual(stock, before)


if __name__ == '__main__':
    unittest.main()
