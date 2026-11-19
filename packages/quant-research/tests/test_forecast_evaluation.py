import unittest

from lamat_quant.forecast_evaluation import evaluate_rolling_mean


class ForecastEvaluationTests(unittest.TestCase):
    def test_explicit_horizon_and_observed_history(self):
        result = evaluate_rolling_mean(range(12), train_end=5, lookback=3, horizon=2)
        first, second = result.forecasts[:2]
        self.assertEqual((first.origin, first.target, first.horizon), (4, 6, 2))
        self.assertEqual((first.prediction, first.actual), (3, 6))
        self.assertEqual((second.origin, second.target, second.prediction), (5, 7, 4))
        self.assertTrue(all(f.target - f.origin == f.horizon for f in result.forecasts))

    def test_future_changes_do_not_change_earlier_forecasts_or_scaling(self):
        original = list(range(12))
        revised = original[:7] + [1000] * 5
        a = evaluate_rolling_mean(original, 5, 3, 2)
        b = evaluate_rolling_mean(revised, 5, 3, 2)
        self.assertEqual((a.train_min, a.train_max), (b.train_min, b.train_max))
        self.assertEqual([f.prediction for f in a.forecasts[:3]],
                         [f.prediction for f in b.forecasts[:3]])
        self.assertNotEqual(a.forecasts[1].actual, b.forecasts[1].actual)

    def test_constant_training_and_invalid_inputs(self):
        self.assertEqual(evaluate_rolling_mean([2, 2, 2, 4], 3, 2, 1).forecasts[0].prediction, 2)
        for values, split, lookback, horizon in [([1, 2], 1, 1, 2), ([1, float('nan'), 3], 2, 1, 1),
                                                  ([1, 2, 3], 1, 2, 1), ([1, 2, 3], 2, 1, 0)]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                evaluate_rolling_mean(values, split, lookback, horizon)


if __name__ == '__main__':
    unittest.main()
