import math
import random
import unittest
from lamat_quant import OUParameters, butterfly, fit_ou


class MeanReversionTests(unittest.TestCase):
    def test_forecast_at_zero_half_life_and_long_horizon(self):
        p = OUParameters(mean=2, theta=0.5, sigma=0.3)
        self.assertEqual(p.forecast(4, 0), (4, 0))
        mean, std = p.forecast(4, p.half_life)
        self.assertAlmostEqual(mean, 3)
        self.assertAlmostEqual(std ** 2, 0.3 ** 2 * (1 - 0.25))
        self.assertAlmostEqual(p.forecast(4, 100)[1], p.stationary_std)

    def test_fit_recovers_synthetic_process(self):
        rng = random.Random(17)
        truth = OUParameters(0.2, 1.5, 0.3)
        dt = 1 / 52
        series = [0.0]
        for _ in range(5000):
            mean, std = truth.forecast(series[-1], dt)
            series.append(rng.gauss(mean, std))
        fitted = fit_ou(series, dt)
        self.assertAlmostEqual(fitted.mean, truth.mean, delta=0.06)
        self.assertAlmostEqual(fitted.theta, truth.theta, delta=0.45)
        self.assertAlmostEqual(fitted.sigma, truth.sigma, delta=0.02)

    def test_butterfly_and_invalid_inputs(self):
        self.assertAlmostEqual(butterfly(4, 3.5, 3), 0)
        for values in ([1, 1, 1, 1], [1, 2, 3, 4], [0, 1, float('nan'), 2]):
            with self.assertRaises(ValueError):
                fit_ou(values, 1)
        with self.assertRaises(ValueError):
            OUParameters(0, 0, 1)
        with self.assertRaises(ValueError):
            OUParameters(0, 1, 1).forecast(0, -1)


if __name__ == '__main__':
    unittest.main()
