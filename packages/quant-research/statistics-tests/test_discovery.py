import unittest

import numpy as np

from lamat_quant.discovery import (adf_summary, fit_pair, fit_pca, hurst_variance_scale,
                                   johansen_summary, pair_cointegration, synthetic_curves)


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.data = synthetic_curves()
        self.train, self.test = self.data[:600], self.data[600:]

    def test_seed_and_chronological_split(self):
        np.testing.assert_array_equal(self.data, synthetic_curves())
        pair, pca = fit_pair(self.train[:, :2]), fit_pca(self.train)
        changed = self.test.copy() + 1000
        self.assertEqual(pair, fit_pair(self.data[:600, :2]))
        np.testing.assert_allclose(pca.components, fit_pca(self.data[:600]).components)
        self.assertFalse(np.allclose(pair.spread(self.test[:, :2]), pair.spread(changed[:, :2])))

    def test_pair_fit_and_cointegration_on_known_data(self):
        pair = fit_pair(self.train[:, :2])
        self.assertAlmostEqual(pair.hedge_ratio, 1.2, delta=0.12)
        self.assertLess(pair_cointegration(self.train[:, :2])['pvalue'], 0.05)
        self.assertLess(adf_summary(pair.spread(self.test[:, :2]))['pvalue'], 0.05)

    def test_pca_explained_variance_and_holdout_transform(self):
        fit = fit_pca(self.train)
        self.assertAlmostEqual(sum(fit.explained_ratio), 1.0)
        self.assertGreater(fit.explained_ratio[0], 0.9)
        np.testing.assert_allclose(fit.components @ fit.components.T, np.eye(3), atol=1e-10)
        np.testing.assert_allclose(fit.transform(self.test), (self.test-fit.centre) @ fit.components.T)
        self.assertEqual(fit.transform(self.test[:1]).shape, (1, 3))
        self.assertEqual(fit_pair(self.train[:, :2]).spread(self.test[:1, :2]).shape, (1,))

    def test_johansen_finds_common_trend_in_synthetic_sample(self):
        result = johansen_summary(self.train)
        self.assertEqual(len(result['trace']), 3)
        self.assertGreater(result['trace'][0], result['critical_95'][0])
        self.assertGreater(result['trace'][1], result['critical_95'][1])

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): hurst_variance_scale(np.ones(200))
        with self.assertRaises(ValueError): adf_summary([1] * 100)
        with self.assertRaises(ValueError): fit_pair(np.ones((100, 2)))
        with self.assertRaises(ValueError): fit_pca(np.array([[np.nan, 1]] * 30))
        with self.assertRaises(ValueError): johansen_summary(np.column_stack((np.arange(50), np.arange(50))))


if __name__ == '__main__':
    unittest.main()
