import copy
import json
from pathlib import Path
import tempfile
import unittest

from lamat_quant import butterfly
from lamat_quant.rates import JsonRatesFixture


FIXTURE = Path(__file__).resolve().parents[3] / 'data/fixtures/synthetic-rates.json'


class RatesFixtureTests(unittest.TestCase):
    def test_fixture_has_provenance_and_expected_butterfly(self):
        data = JsonRatesFixture(FIXTURE).load()
        self.assertEqual(data.provenance.units, 'percent per annum')
        self.assertIn('synthetic', data.provenance.source.lower())
        row = data.observations[0]
        self.assertEqual(row.observation_date.isoformat(), '2024-01-05')
        self.assertAlmostEqual(butterfly(row.two_year, row.five_year, row.ten_year), 0.1)

    def test_invalid_data_and_provenance_are_rejected(self):
        original = json.loads(FIXTURE.read_text(encoding='utf-8'))
        cases = []
        missing = copy.deepcopy(original)
        del missing['observations'][0]['5y']
        cases.append(missing)
        nonfinite = copy.deepcopy(original)
        nonfinite['observations'][0]['2y'] = float('nan')
        cases.append(nonfinite)
        duplicate = copy.deepcopy(original)
        duplicate['observations'][1]['date'] = duplicate['observations'][0]['date']
        cases.append(duplicate)
        units = copy.deepcopy(original)
        units['provenance']['units'] = 'basis points'
        cases.append(units)
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / 'fixture.json'
                path.write_text(json.dumps(case), encoding='utf-8')
                with self.assertRaises(ValueError):
                    JsonRatesFixture(path).load()
