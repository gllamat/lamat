import math
import unittest

from lamat_quant.option_spreads import interval_survival


class OptionSpreadTests(unittest.TestCase):
    def test_unequal_strikes_use_each_own_gap(self):
        rows = interval_survival([90, 100, 120], [16, 9, 1], 1)
        self.assertAlmostEqual(rows[0].average_survival, .7)
        self.assertAlmostEqual(rows[1].average_survival, .4)
        self.assertLess(16 - 2 * 9 + 1, 0)  # Unweighted butterfly is misleading here.

    def test_synthetic_distribution_and_discount(self):
        states = [(80, .2), (105, .5), (140, .3)]
        strikes = [90, 100, 120, 145]
        discount = .95
        calls = [discount * sum(p * max(s - k, 0) for s, p in states) for k in strikes]
        rows = interval_survival(strikes, calls, discount)
        for actual, expected in zip(rows, [.8, .425, .24]):
            self.assertAlmostEqual(actual.average_survival, expected)
        self.assertEqual((rows[0].lower_strike, rows[-1].upper_strike), (90, 145))

    def test_invalid_quotes_rejected(self):
        cases = [([1, 1], [1, 0], 1), ([1, 2], [1, 2], 1),
                 ([1, 2], [2, 0], 1), ([1, 2, 4], [1, .9, 0], 1),
                 ([1, 2], [1, 0], 0), ([1, math.nan], [1, 0], 1),
                 ([1, 2], [1], 1), ([-1, 2], [1, 0], 1)]
        for args in cases:
            with self.subTest(args=args), self.assertRaises(ValueError):
                interval_survival(*args)


if __name__ == '__main__':
    unittest.main()
