import unittest

from stock import adjust_many, adjust_stock


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


class BatchStockTests(unittest.TestCase):
    def test_success_returns_final_touched_quantities_and_preserves_inputs(self):
        for adjustments, expected, final_stock in (
            ([('A', 2), ('B', -9)], {'A': 7, 'B': 0}, {'A': 7, 'B': 0, 'C': 4}),
            ([('A', -5), ('A', 3), ('A', -1)], {'A': 2}, {'A': 2, 'B': 9, 'C': 4}),
            ([('A', 0)], {'A': 5}, {'A': 5, 'B': 9, 'C': 4}),
            ([('A', -5), ('A', 0)], {'A': 0}, {'A': 0, 'B': 9, 'C': 4}),
        ):
            with self.subTest(adjustments=adjustments):
                stock = {'A': 5, 'B': 9, 'C': 4}
                alias = stock
                before_adjustments = adjustments.copy()
                result = adjust_many(stock, adjustments)
                self.assertEqual(result, expected)
                self.assertEqual(alias, final_stock)
                self.assertEqual(adjustments, before_adjustments)
                result['A'] = 100
                self.assertEqual(stock, final_stock)

    def test_replenishment_precedes_withdrawal(self):
        stock = {'A': 0, 'B': 9}
        self.assertEqual(adjust_many(stock, [('A', 3), ('A', -3)]), {'A': 0})
        self.assertEqual(stock, {'A': 0, 'B': 9})

    def test_failures_preserve_all_stock_and_adjustments(self):
        for adjustments, error_type, error_args in (
            ([('A', 2), ('missing', 1)], KeyError, ('missing',)),
            ([('A', 2), ('B', -10)], ValueError, ('Negative stock',)),
            ([('A', -3), ('A', -3), ('A', 2)], ValueError, ('Negative stock',)),
            ([('A', -6), ('missing', 1)], ValueError, ('Negative stock',)),
            ([('missing', 0), ('A', -6)], KeyError, ('missing',)),
        ):
            with self.subTest(adjustments=adjustments):
                stock = {'A': 5, 'B': 9, 'C': 4}
                before_stock = stock.copy()
                before_adjustments = adjustments.copy()
                with self.assertRaises(error_type) as error:
                    adjust_many(stock, adjustments)
                self.assertEqual(error.exception.args, error_args)
                self.assertEqual(stock, before_stock)
                self.assertEqual(adjustments, before_adjustments)

    def test_unknown_product_in_empty_stock(self):
        stock = {}
        adjustments = [('missing', 0)]
        with self.assertRaises(KeyError) as error:
            adjust_many(stock, adjustments)
        self.assertEqual(error.exception.args, ('missing',))
        self.assertEqual(stock, {})
        self.assertEqual(adjustments, [('missing', 0)])

    def test_empty_adjustments(self):
        for stock in ({}, {'A': 5, 'B': 9}):
            with self.subTest(stock=stock):
                before = stock.copy()
                adjustments = []
                self.assertEqual(adjust_many(stock, adjustments), {})
                self.assertEqual(stock, before)
                self.assertEqual(adjustments, [])


if __name__ == '__main__':
    unittest.main()
