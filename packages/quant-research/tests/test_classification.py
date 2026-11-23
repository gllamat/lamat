import unittest

from lamat_quant.classification import binary_metrics


class BinaryMetricsTests(unittest.TestCase):
    def test_imbalanced_accuracy_and_recall(self):
        metrics = binary_metrics([1] + [0] * 99, [0] * 100)
        self.assertEqual(metrics.accuracy, .99)
        self.assertEqual(metrics.recall, 0)
        self.assertIsNone(metrics.precision)
        self.assertEqual(metrics.false_positive_rate, 0)

    def test_confusion_counts_and_rates(self):
        metrics = binary_metrics([1, 1, 0, 0, 0], [1, 0, 1, 0, 0])
        self.assertEqual((metrics.true_positive, metrics.false_positive,
                          metrics.true_negative, metrics.false_negative), (1, 1, 2, 1))
        self.assertEqual(metrics.precision, .5)
        self.assertEqual(metrics.recall, .5)
        self.assertAlmostEqual(metrics.false_positive_rate, 1 / 3)
        self.assertEqual(metrics.accuracy, .6)

    def test_absent_classes_are_undefined(self):
        metrics = binary_metrics([1, 1], [1, 0])
        self.assertIsNone(metrics.false_positive_rate)
        self.assertEqual(metrics.recall, .5)
        self.assertIsNone(binary_metrics([0], [0]).recall)

    def test_invalid_labels_and_lengths(self):
        for actual, predicted in (([], []), ([0], []), ([2], [0]), ([0], [-1])):
            with self.subTest(actual=actual, predicted=predicted):
                with self.assertRaises(ValueError):
                    binary_metrics(actual, predicted)


if __name__ == "__main__":
    unittest.main()
