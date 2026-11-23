import unittest

from lamat_quant.additive_explanation import explain_linear_score


class LinearExplanationTests(unittest.TestCase):
    def test_reference_baseline_and_score_reconstruction(self):
        weights = {"a": 2.0, "b": -0.5}
        explanation = explain_linear_score(0.1, weights, {"a": 3, "b": 4},
                                           {"a": 1, "b": 2})
        self.assertAlmostEqual(explanation.baseline, 1.1)
        self.assertEqual(dict(explanation.contributions), {"a": 4.0, "b": -1.0})
        self.assertAlmostEqual(explanation.score, 4.1)
        self.assertAlmostEqual(explanation.score, 0.1 + 2.0 * 3 - .5 * 4)

    def test_reference_changes_attribution_not_score(self):
        args = (1.0, {"x": 2.0}, {"x": 3.0})
        first = explain_linear_score(*args, {"x": 0.0})
        second = explain_linear_score(*args, {"x": 2.0})
        self.assertEqual(first.score, second.score)
        self.assertNotEqual(first.baseline, second.baseline)
        self.assertNotEqual(first.contributions, second.contributions)

    def test_mismatched_or_nonfinite_inputs(self):
        for weights, features, reference in [({}, {}, {}),
                                              ({"x": 1}, {"y": 1}, {"x": 1}),
                                              ({"x": float("nan")}, {"x": 1}, {"x": 1})]:
            with self.subTest(weights=weights):
                with self.assertRaises(ValueError):
                    explain_linear_score(0, weights, features, reference)
