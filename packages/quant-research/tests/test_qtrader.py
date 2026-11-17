import random
import unittest
from lamat_quant.qtrader import Config, evaluate, generate_path, greedy_action, state, train, transition


class QTraderTests(unittest.TestCase):
    def setUp(self):
        self.cfg = Config(cost=0.1)

    def test_target_position_timing_cost_and_liquidation(self):
        holding, gross, cost, net = transition(10, 0, 1, 11, self.cfg)
        self.assertEqual((holding, gross), (1, 1))
        self.assertAlmostEqual(cost, .1)
        self.assertAlmostEqual(net, .9)
        holding, gross, cost, net = transition(11, 1, -1, 10, self.cfg, terminal=True)
        self.assertEqual((holding, gross), (0, 1))
        self.assertAlmostEqual(cost, .3)
        self.assertAlmostEqual(net, .7)

    def test_ties_prefer_flat_and_future_prices_do_not_choose_action(self):
        key = state(10, 0, self.cfg)
        self.assertEqual(greedy_action({}, key), 1)
        self.assertEqual(greedy_action({key: (1, 1, 1)}, key), 1)
        action = (-1, 0, 1)[greedy_action({key: (0, 0, 2)}, key)]
        self.assertEqual(action, 1)
        self.assertEqual(transition(10, 0, action, 9, self.cfg)[1], -1)
        self.assertEqual(transition(10, 0, action, 11, self.cfg)[1], 1)

    def test_deterministic_frozen_out_of_sample_evaluation(self):
        a = train(self.cfg, episodes=5, steps=10, seed=11)
        self.assertEqual(a, train(self.cfg, episodes=5, steps=10, seed=11))
        snapshot = dict(a)
        self.assertEqual(evaluate(self.cfg, a, episodes=3, steps=10, seed=20), evaluate(self.cfg, a, episodes=3, steps=10, seed=20))
        self.assertEqual(a, snapshot)
        self.assertNotEqual(generate_path(self.cfg, 10, random.Random(11)), generate_path(self.cfg, 10, random.Random(20)))
        self.assertTrue(all(x == (0., 0., 0.) for x in evaluate(self.cfg, a, episodes=3, steps=10, policy='flat')))

    def test_validation_and_bounded_prices(self):
        self.assertTrue(all(self.cfg.lower <= x <= self.cfg.upper for x in generate_path(self.cfg, 200, random.Random(1))))
        with self.assertRaises(ValueError): Config(cost=-1)
        with self.assertRaises(ValueError): generate_path(self.cfg, 0, random.Random(1))
        with self.assertRaises(ValueError): transition(10, 0, 2, 10, self.cfg)
        with self.assertRaises(ValueError): train(self.cfg, episodes=1, steps=5, epsilon=2)
        with self.assertRaises(ValueError): evaluate(self.cfg, {}, policy='invalid')

if __name__ == '__main__':
    unittest.main()
