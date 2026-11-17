import unittest
from datetime import date, timedelta

import numpy as np

from lamat_quant.regimes import fit_regimes


class RegimeTests(unittest.TestCase):
    def setUp(self):
        self.dates = [date(2020, 1, 1) + timedelta(days=i) for i in range(12)]
        self.curves = np.array([[i, i*i + 2, i % 3 + i] for i in range(12)], dtype=float)

    def test_training_fits_are_invariant_to_future_data(self):
        baseline = fit_regimes(self.dates, self.curves, 8, clusters=2)
        changed = self.curves.copy()
        changed[8:] += 10000
        alternate = fit_regimes(self.dates, changed, 8, clusters=2)
        np.testing.assert_allclose(baseline.scaler.mean_, alternate.scaler.mean_)
        np.testing.assert_allclose(baseline.pca.components_, alternate.pca.components_)
        np.testing.assert_allclose(baseline.clusters.cluster_centers_, alternate.clusters.cluster_centers_)
        np.testing.assert_array_equal(baseline.labels[:8], alternate.labels[:8])
        np.testing.assert_allclose(baseline.scaler.mean_, self.curves[:8].mean(axis=0))
        np.testing.assert_array_equal(baseline.labels[8:], baseline.clusters.predict(
            baseline.pca.transform(baseline.scaler.transform(self.curves[8:]))))

    def test_reproducible_and_date_aligned(self):
        a = fit_regimes(self.dates, self.curves, 8, clusters=2)
        b = fit_regimes(self.dates, self.curves, 8, clusters=2)
        np.testing.assert_array_equal(a.labels, b.labels)
        self.assertEqual(a.dates, tuple(self.dates))
        self.assertEqual(a.scores.shape, (12, 2))

    def test_invalid_data_rejected(self):
        bad = self.curves.copy()
        bad[0, 1] = np.nan
        for dates, curves, split in [(self.dates[::-1], self.curves, 8),
                                      (self.dates, bad, 8), (self.dates, self.curves, 12),
                                      (self.dates, np.ones((12, 3)), 8)]:
            with self.subTest(split=split):
                with self.assertRaises(ValueError): fit_regimes(dates, curves, split, clusters=2)


if __name__ == '__main__':
    unittest.main()
