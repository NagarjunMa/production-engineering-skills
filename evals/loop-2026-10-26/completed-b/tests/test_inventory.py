import unittest

from stock import adjust_many, adjust_stock


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


class BatchStockTests(unittest.TestCase):
    def test_success_uses_tentative_quantities_and_returns_touched_products(self):
        stock = {'A': 5, 'B': 0, 'untouched': 9}
        adjustments = [('A', -4), ('B', 3), ('A', 2), ('B', -3)]
        before = adjustments.copy()
        self.assertEqual(adjust_many(stock, adjustments), {'A': 3, 'B': 0})
        self.assertEqual(stock, {'A': 3, 'B': 0, 'untouched': 9})
        self.assertEqual(adjustments, before)

    def test_zero_adjustment_still_returns_touched_product(self):
        stock = {'A': 0, 'B': 9}
        self.assertEqual(adjust_many(stock, [('A', 0)]), {'A': 0})
        self.assertEqual(stock, {'A': 0, 'B': 9})

    def test_empty_batch_returns_empty_without_changing_inputs(self):
        for initial in ({}, {'A': 5, 'B': 9}):
            with self.subTest(initial=initial):
                stock = initial.copy()
                adjustments = []
                self.assertEqual(adjust_many(stock, adjustments), {})
                self.assertEqual(stock, initial)
                self.assertEqual(adjustments, [])

    def test_late_failure_rolls_back_every_product_and_preserves_adjustments(self):
        for rejected, error in ((('missing', 1), KeyError),
                                (('B', -11), ValueError)):
            with self.subTest(rejected=rejected):
                stock = {'A': 5, 'B': 9}
                adjustments = [('A', -2), ('B', 1), rejected]
                before = adjustments.copy()
                with self.assertRaises(error):
                    adjust_many(stock, adjustments)
                self.assertEqual(stock, {'A': 5, 'B': 9})
                self.assertEqual(adjustments, before)

    def test_intermediate_underflow_is_rejected_even_if_restored_later(self):
        stock = {'A': 5, 'B': 9}
        adjustments = [('A', -6), ('A', 6)]
        before = adjustments.copy()
        with self.assertRaisesRegex(ValueError, '^Negative stock$'):
            adjust_many(stock, adjustments)
        self.assertEqual(stock, {'A': 5, 'B': 9})
        self.assertEqual(adjustments, before)

    def test_first_invalid_pair_determines_error(self):
        for adjustments, error, args in (
                ([('missing', -1), ('A', -6)], KeyError, ('missing',)),
                ([('A', -6), ('missing', -1)], ValueError, ('Negative stock',))):
            with self.subTest(adjustments=adjustments):
                stock = {'A': 5, 'B': 9}
                before = adjustments.copy()
                with self.assertRaises(error) as raised:
                    adjust_many(stock, adjustments)
                self.assertEqual(raised.exception.args, args)
                self.assertEqual(stock, {'A': 5, 'B': 9})
                self.assertEqual(adjustments, before)


if __name__ == '__main__':
    unittest.main()
