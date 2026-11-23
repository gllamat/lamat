import math
import unittest
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from lamat_quant.return_distributions import distribution_points, elapsed_log_returns


class ReturnDistributionTests(unittest.TestCase):
    def setUp(self):
        self.t = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.minute = timedelta(minutes=1)

    def test_exact_elapsed_horizon_skips_gaps(self):
        obs = [(self.t, 100), (self.t + self.minute, 200),
               (self.t + 3 * self.minute, 100)]
        one = elapsed_log_returns(obs, self.minute)
        self.assertEqual(len(one), 1)
        self.assertEqual((one[0].start, one[0].end), (self.t, self.t + self.minute))
        self.assertAlmostEqual(one[0].log_return, math.log(2))
        two = elapsed_log_returns(obs, 2 * self.minute)
        self.assertEqual(len(two), 1)
        self.assertAlmostEqual(two[0].log_return, -math.log(2))

    def test_dst_uses_elapsed_time(self):
        london = ZoneInfo('Europe/London')
        before = datetime(2026, 10, 25, 1, 30, tzinfo=london, fold=0)
        after = datetime(2026, 10, 25, 1, 30, tzinfo=london, fold=1)
        result = elapsed_log_returns([(before, 100), (after, 110)], timedelta(hours=1))
        self.assertEqual(len(result), 1)
        self.assertAlmostEqual(result[0].log_return, math.log(1.1))

    def test_ecdf_collapses_ties_at_right_continuous_probability(self):
        self.assertEqual(distribution_points([0, 0, 1])['ecdf'], ((0, 2/3), (1, 1)))

    def test_validation(self):
        for obs, horizon in [([(self.t, 0)], self.minute),
                             ([(self.t, float('nan'))], self.minute),
                             ([(self.t.replace(tzinfo=None), 1)], self.minute),
                             ([(self.t, 1), (self.t, 2)], self.minute),
                             ([(self.t, 1)], timedelta(0))]:
            with self.subTest(obs=obs, horizon=horizon), self.assertRaises(ValueError):
                elapsed_log_returns(obs, horizon)
        for values in ([], [1], [1, 1], [1, float('nan')]):
            with self.subTest(values=values), self.assertRaises(ValueError):
                distribution_points(values)

    def test_distribution_uses_observed_returns_for_both_diagnostics(self):
        points = distribution_points([.2, -.1, 0])
        self.assertEqual([x for x, _ in points['ecdf']], [-.1, 0, .2])
        self.assertEqual([y for _, y in points['qq']], [-.1, 0, .2])
        self.assertEqual([y for _, y in points['ecdf']], [1/3, 2/3, 1])
        self.assertLess(points['qq'][0][0], points['qq'][1][0])
        self.assertAlmostEqual(points['mean'], 1/30)


if __name__ == '__main__':
    unittest.main()
