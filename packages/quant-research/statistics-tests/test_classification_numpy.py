import unittest

import numpy as np

from lamat_quant.classification import binary_metrics


class ClassificationNumpyTests(unittest.TestCase):
    def test_binary_vectors_and_invalid_inputs(self):
        metrics = binary_metrics(np.array([1, 1, 0, 0]), np.array([1, 0, 1, 0]))
        self.assertEqual((metrics.true_positive, metrics.false_positive,
                          metrics.true_negative, metrics.false_negative), (1, 1, 1, 1))
        self.assertEqual(metrics.precision, .5)
        with self.assertRaises(ValueError):
            binary_metrics(np.array([]), np.array([]))
        with self.assertRaises(ValueError):
            binary_metrics(np.array([0, 2]), np.array([0, 1]))
