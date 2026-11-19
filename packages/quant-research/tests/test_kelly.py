import math
import unittest

from lamat_quant.kelly import Scenario, expected_log_growth, grid_search


class KellyTests(unittest.TestCase):
    def test_single_event_matches_analytical_even_odds_optimum(self):
        outcomes = [Scenario(.75, (1.,)), Scenario(.25, (-1.,))]
        allocation, value = grid_search(outcomes, steps=20)
        self.assertEqual(allocation, (.5,))
        self.assertAlmostEqual(value, .75 * math.log(1.5) + .25 * math.log(.5))
        self.assertGreater(value, expected_log_growth(outcomes, (0.,)))

    def test_fair_game_prefers_no_stake(self):
        outcomes = [Scenario(.5, (1.,)), Scenario(.5, (-1.,))]
        self.assertEqual(grid_search(outcomes, steps=10), ((0.,), 0.))
        self.assertLess(expected_log_growth(outcomes, (.1,)), 0.)

    def test_joint_distribution_changes_growth(self):
        independent = [Scenario(.25, (1., 1.)), Scenario(.25, (1., -1.)),
                       Scenario(.25, (-1., 1.)), Scenario(.25, (-1., -1.))]
        correlated = [Scenario(.5, (1., 1.)), Scenario(.5, (-1., -1.))]
        self.assertGreater(expected_log_growth(independent, (.25, .25)),
                           expected_log_growth(correlated, (.25, .25)))

    def test_two_event_synthetic_grid_result(self):
        scenarios = [Scenario(.33, (1., 1.)), Scenario(.27, (1., -1.)),
                     Scenario(.22, (-1., 1.)), Scenario(.18, (-1., -1.))]
        allocation, growth = grid_search(scenarios, steps=20)
        self.assertEqual(allocation, (.2, .1))
        self.assertAlmostEqual(growth, .33 * math.log(1.3) + .27 * math.log(1.1)
                               + .22 * math.log(.9) + .18 * math.log(.7))

    def test_wealth_boundary_and_zero_probability(self):
        possible_loss = [Scenario(.5, (1.,)), Scenario(.5, (-1.,))]
        with self.assertRaises(ValueError):
            expected_log_growth(possible_loss, (1.,))
        impossible_loss = [Scenario(1., (1.,)), Scenario(0., (-1.,))]
        self.assertAlmostEqual(expected_log_growth(impossible_loss, (1.,)), math.log(2))
        self.assertEqual(grid_search(impossible_loss, steps=10)[0], (1.,))

    def test_invalid_inputs_and_grid_cap(self):
        good = [Scenario(.5, (1.,)), Scenario(.5, (-1.,))]
        for bad in [[], [Scenario(.2, (1.,))], [Scenario(float('nan'), (1.,))],
                    [Scenario(1., (float('inf'),))], [Scenario(1., (-1.1,))],
                    [Scenario(.5, (1.,)), Scenario(.5, (1., 1.))]]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                expected_log_growth(bad, (0.,))
        for allocation in [(-.1,), (1.1,), (float('nan'),), (0., 0.)]:
            with self.subTest(allocation=allocation), self.assertRaises(ValueError):
                expected_log_growth(good, allocation)
        for steps in (0, True, 1.5):
            with self.subTest(steps=steps), self.assertRaises(ValueError):
                grid_search(good, steps=steps)
        with self.assertRaises(ValueError):
            grid_search([Scenario(1., (0.,) * 8)], steps=100)


if __name__ == '__main__':
    unittest.main()
