import unittest
from datetime import date
from lamat_quant.sentiment import Entity, evaluate, resolve_entities, score_sentiment


class SentimentTests(unittest.TestCase):
    def setUp(self):
        self.registry = [Entity('AMC', date(2021, 1, 1), date(2022, 1, 1))]

    def test_ambiguous_terms_are_not_tickers(self):
        self.assertEqual(resolve_entities('YOLO HOLD $AMC', date(2021, 2, 1), self.registry), ['AMC'])
        self.assertEqual(resolve_entities('YOLO HOLD', date(2021, 2, 1), self.registry), [])

    def test_point_in_time_and_token_boundaries(self):
        self.assertEqual(resolve_entities('$AMC', date(2020, 12, 31), self.registry), [])
        self.assertEqual(resolve_entities('$AMC', date(2022, 1, 1), self.registry), [])
        self.assertEqual(resolve_entities('a$AMC $AMCX $amc $AMC', date(2021, 2, 1), self.registry), ['AMC'])

    def test_synthetic_scoring_and_reported_negation_failure(self):
        self.assertEqual(score_sentiment('profit growth'), 'positive')
        self.assertEqual(score_sentiment('not a loss'), 'negative')
        report = evaluate([{'date':'2021-02-01','text':'$AMC did not report a loss',
                            'entities':['AMC'],'sentiment':'positive'}], self.registry)
        self.assertEqual(report['entity_exact_accuracy'], 1.0)
        self.assertEqual(report['sentiment_accuracy'], 0.0)

    def test_empty_evaluation_rejected(self):
        with self.assertRaises(ValueError): evaluate([], self.registry)
