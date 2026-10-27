import unittest

from inventory import adjust_stock


class StockTests(unittest.TestCase):
    def test_increase(self):
        stock = {'A': 5}
        self.assertEqual(adjust_stock(stock, 'A', 2), 7)


if __name__ == '__main__':
    unittest.main()
