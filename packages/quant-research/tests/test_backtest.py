import math
import unittest

from lamat_quant.backtest import ThresholdRule, evaluate_chronologically, run_backtest, simulate_ou
from lamat_quant.mean_reversion import OUParameters


class BacktestTests(unittest.TestCase):
    def test_long_trade_and_terminal_liquidation_cost(self):
        r = run_backtest([-2, -1, 0], ThresholdRule(0, 1, size=2), .1)
        self.assertEqual([x.position_after for x in r.rows], [2, 2, 0])
        self.assertAlmostEqual(r.gross_pnl, 4)
        self.assertAlmostEqual(r.costs, .4)
        self.assertAlmostEqual(r.net_pnl, 3.6)
        self.assertAlmostEqual(r.rows[-1].cumulative_net_pnl, 3.6)

    def test_short_exit_and_no_same_bar_flip(self):
        r = run_backtest([2, -2, -3, 0], ThresholdRule(0, 1), .2)
        self.assertEqual([x.position_after for x in r.rows], [-1, 0, 1, 0])
        self.assertAlmostEqual(r.gross_pnl, 7)
        self.assertAlmostEqual(r.costs, .8)
        self.assertAlmostEqual(r.net_pnl, 6.2)

    def test_signal_cannot_earn_pre_entry_move(self):
        r = run_backtest([0, -2, -1], ThresholdRule(0, 1), 0)
        self.assertEqual(r.rows[1].gross_pnl, 0)
        self.assertEqual(r.rows[2].gross_pnl, 1)

    def test_chronological_split_is_flat_and_excludes_boundary_return(self):
        train, test = evaluate_chronologically([-2, -1, -100, -99], 2, ThresholdRule(0, 1), .25)
        self.assertEqual(train.net_pnl, .5)
        self.assertEqual(test.net_pnl, .5)
        self.assertEqual(train.rows[-1].position_after, 0)
        self.assertEqual(test.rows[0].position_before, 0)
        self.assertEqual(test.rows[0].gross_pnl, 0)

    def test_seed_and_future_changes_leave_prior_rows_unchanged(self):
        p = OUParameters(0, 1, .2)
        a = simulate_ou(p, 0, .1, 20, 42)
        self.assertEqual(a, simulate_ou(p, 0, .1, 20, 42))
        self.assertNotEqual(a, simulate_ou(p, 0, .1, 20, 43))
        rule = ThresholdRule(0, .05)
        altered = a[:10] + (100.,) + a[11:]
        self.assertEqual(run_backtest(a, rule, .01).rows[:10], run_backtest(altered, rule, .01).rows[:10])

    def test_invalid_values_and_boundaries(self):
        for args in ((0, 0, 0, 1), (0, 1, 1, 1), (0, 1, -1, 1), (0, 1, 0, 0), (math.nan, 1, 0, 1)):
            with self.assertRaises(ValueError): ThresholdRule(*args)
        for marks, cost in (([0], 0), ([0, math.inf], 0), ([0, 1], -1), ([0, 1], math.nan)):
            with self.assertRaises(ValueError): run_backtest(marks, ThresholdRule(0, 1), cost)
        for split in (0, 1, 3, 4, True):
            with self.assertRaises(ValueError): evaluate_chronologically([0, 1, 2, 3], split, ThresholdRule(0, 1), 0)
        for steps in (0, True, 1.5):
            with self.assertRaises(ValueError): simulate_ou(OUParameters(0, 1, .2), 0, 1, steps, 42)

if __name__ == '__main__':
    unittest.main()
