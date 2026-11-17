"""Checks against analytical values, independent of the simulation example."""
import math
import unittest

from lamat_quant import OUParameters, fit_ou


class OUAnalyticalValidation(unittest.TestCase):
    def test_known_conditional_transition(self):
        # With theta=ln(2), half the initial deviation remains after one unit.
        p = OUParameters(mean=1.0, theta=math.log(2), sigma=0.2)
        mean, standard_deviation = p.forecast(3.0, 1.0)
        self.assertAlmostEqual(mean, 2.0)
        self.assertAlmostEqual(standard_deviation ** 2, 0.04 * 0.75 / (2 * math.log(2)))
        self.assertAlmostEqual(p.half_life, 1.0)

    def test_exact_ar_sequence_and_time_unit_conversion(self):
        # y = 1 + x/2 exactly, giving mean=2 and theta=ln(2)/dt.
        values = [1.0, 1.5, 1.75, 1.875, 1.9375]
        unit = fit_ou(values, 1.0)
        quarter = fit_ou(values, 0.25)
        self.assertAlmostEqual(unit.mean, 2.0)
        self.assertAlmostEqual(unit.theta, math.log(2))
        self.assertAlmostEqual(unit.sigma, 0.0)
        self.assertAlmostEqual(quarter.theta, 4 * unit.theta)
        self.assertAlmostEqual(quarter.half_life, unit.half_life / 4)
        noisy = [1.0, 1.5, 1.6, 1.8, 1.7, 1.85]
        unit = fit_ou(noisy, 1.0)
        quarter = fit_ou(noisy, 0.25)
        self.assertGreater(unit.sigma, 0)
        self.assertAlmostEqual(quarter.sigma, 2 * unit.sigma)

    def test_zero_noise_and_tiny_horizon(self):
        p = OUParameters(mean=1, theta=2, sigma=0)
        self.assertEqual(p.forecast(3, 0)[1], 0)
        self.assertEqual(p.forecast(3, 0.5)[1], 0)
        p = OUParameters(mean=0, theta=1, sigma=0.3)
        _, stdev = p.forecast(0, 1e-12)
        self.assertAlmostEqual(stdev ** 2 / 1e-12, 0.09, places=10)

    def test_invalid_parameter_and_time_inputs(self):
        for args in [(0, -1, 1), (0, 1, -1), (float('inf'), 1, 1)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                OUParameters(*args)
        for dt in (0, -1, float('inf')):
            with self.subTest(dt=dt), self.assertRaises(ValueError):
                fit_ou([1, 1.5, 1.75, 1.875], dt)
