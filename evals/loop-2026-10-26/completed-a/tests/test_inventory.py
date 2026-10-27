import unittest

from inventory import adjust_stock


class StockTests(unittest.TestCase):
    def test_increase(self):
        stock = {'A': 5}
        self.assertEqual(adjust_stock(stock, 'A', 2), 7)

    def test_successful_adjustments(self):
        for starting, delta, expected in ((5, 2, 7), (5, 0, 5), (5, -2, 3),
                                          (5, -5, 0), (0, 0, 0), (0, 2, 2)):
            with self.subTest(starting=starting, delta=delta):
                stock = {'A': starting, 'B': 9}
                self.assertEqual(adjust_stock(stock, 'A', delta), expected)
                self.assertEqual(stock, {'A': expected, 'B': 9})

    def test_negative_result_leaves_entire_stock_unchanged(self):
        for starting, delta in ((5, -6), (0, -1)):
            with self.subTest(starting=starting, delta=delta):
                stock = {'A': starting, 'B': 9}
                before = stock.copy()
                with self.assertRaises(ValueError):
                    adjust_stock(stock, 'A', delta)
                self.assertEqual(stock, before)

    def test_unknown_product_leaves_entire_stock_unchanged(self):
        for initial in ({}, {'A': 5, 'B': 9}):
            for delta in (2, 0, -2):
                with self.subTest(initial=initial, delta=delta):
                    stock = initial.copy()
                    with self.assertRaises(KeyError):
                        adjust_stock(stock, 'missing', delta)
                    self.assertEqual(stock, initial)


if __name__ == '__main__':
    unittest.main()
