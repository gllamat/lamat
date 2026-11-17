"""A reproducible synthetic example; rates are illustrative, not market data."""
import random
from pathlib import Path
from lamat_quant import OUParameters, butterfly, fit_ou
from lamat_quant.rates import JsonRatesFixture

rng = random.Random(2026)
truth = OUParameters(mean=0.0, theta=1.5, sigma=0.30)
dt = 1 / 52  # one week, with model time measured in years
series = [0.30]
for _ in range(520):
    expected, uncertainty = truth.forecast(series[-1], dt)
    series.append(rng.gauss(expected, uncertainty))
fit = fit_ou(series, dt)
expected, uncertainty = fit.forecast(series[-1], 0.5)
fixture = Path(__file__).resolve().parents[1] / 'data/fixtures/synthetic-rates.json'
rates = JsonRatesFixture(fixture).load()
latest = rates.observations[-1]
print('Source:', rates.provenance.source)
print('Rate units:', rates.provenance.units)
print('Synthetic 2s/5s/10s butterfly on', latest.observation_date, ':',
      butterfly(latest.two_year, latest.five_year, latest.ten_year))
print(f'OU fit: mean={fit.mean:.3f}, theta/year={fit.theta:.3f}, sigma/sqrt(year)={fit.sigma:.3f}')
print(f'Half-life: {fit.half_life:.3f} years')
print(f'Six-month conditional mean={expected:.3f}; standard deviation={uncertainty:.3f}')
