from datetime import date, datetime
import unittest

from lamat_quant.date_alignment import align_by_date


class DateAlignmentTests(unittest.TestCase):
    def test_gaps_and_order_do_not_pair_different_dates(self):
        d1, d2, d3 = (date(2020, 1, n) for n in (1, 2, 3))
        result = align_by_date([(d3, 103), (d1, 101), (d2, 102)],
                               [(d3, 203), (d1, 201)])
        self.assertEqual(result.matched, ((d1, 101., 201.), (d3, 103., 203.)))
        self.assertEqual(result.left_only, (d2,))
        self.assertEqual(result.right_only, ())

    def test_unmatched_and_empty_series(self):
        d1, d2 = date(2020, 1, 1), date(2020, 1, 2)
        result = align_by_date([(d1, 1)], [(d2, 2)])
        self.assertEqual(result.matched, ())
        self.assertEqual(result.left_only, (d1,))
        self.assertEqual(result.right_only, (d2,))
        self.assertEqual(align_by_date([], []).matched, ())

    def test_duplicate_invalid_prices_and_timestamps_rejected(self):
        d = date(2020, 1, 1)
        for rows in ([(d, 1), (d, 2)], [(d, 0)], [(d, float('nan'))],
                     [(datetime(2020, 1, 1), 1)]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                align_by_date(rows, [])
