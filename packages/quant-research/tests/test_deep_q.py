import random
import unittest

from lamat_quant.deep_q import Network, action_index, evaluate_neural, features, train_neural
from lamat_quant.qtrader import Config, evaluate


class DeepQTests(unittest.TestCase):
    def test_network_update_reduces_selected_output_error_and_copy_is_independent(self):
        model = Network(random.Random(5))
        frozen = model.copy()
        x = (.2, 1.)
        before = model.values(x)
        model.update(x, 2, before[2] + .5, .01)
        self.assertGreater(model.values(x)[2], before[2])
        self.assertEqual(frozen.values(x), before)

    def test_frozen_evaluation_is_repeatable(self):
        cfg = Config()
        a = train_neural(cfg, episodes=3, steps=8, seed=5)
        b = train_neural(cfg, episodes=3, steps=8, seed=5)
        before = a.values(features(10, 0, cfg))
        self.assertEqual(before, b.values(features(10, 0, cfg)))
        first = evaluate_neural(cfg, a, episodes=3, steps=8, seed=88)
        self.assertEqual(first, evaluate_neural(cfg, a, episodes=3, steps=8, seed=88))
        self.assertEqual(before, a.values(features(10, 0, cfg)))
        self.assertTrue(all(abs(g - c - n) < 1e-9 for g, c, n in first))

    def test_shared_paths_and_terminal_cost(self):
        cfg = Config(cost=.1)
        # A network that always selects flat matches the tabular flat policy.
        class Flat:
            def values(self, x): return (0., 1., 0.)
        self.assertEqual(evaluate_neural(cfg, Flat(), episodes=3, steps=10, seed=42),
                         evaluate(cfg, {}, episodes=3, steps=10, seed=42, policy='flat'))
        class Long:
            def values(self, x): return (0., 0., 1.)
        one = evaluate_neural(cfg, Long(), episodes=1, steps=1, seed=42)[0]
        self.assertAlmostEqual(one[1], .2)  # opening and terminal liquidation
        self.assertEqual(action_index((1, 1, 1)), 1)

    def test_validation(self):
        cfg = Config()
        for kwargs in ({'episodes': 0}, {'steps': 0}, {'target_interval': 0}, {'rate': float('nan')}, {'epsilon': 2}):
            with self.assertRaises(ValueError): train_neural(cfg, **kwargs)
        with self.assertRaises(ValueError): features(10, 2, cfg)

if __name__ == '__main__':
    unittest.main()
