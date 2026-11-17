"""A reproducible synthetic example; rates are illustrative, not market data."""
import random
from lamat_quant import OUParameters, butterfly, fit_ou

rng = random.Random(2026)
truth = OUParameters(mean=0.0, theta=1.5, sigma=0.30)
dt = 1 / 52  # one week, with model time measured in years
series = [0.30]
for _ in range(520):
    expected, uncertainty = truth.forecast(series[-1], dt)
    series.append(rng.gauss(expected, uncertainty))
fit = fit_ou(series, dt)
expected, uncertainty = fit.forecast(series[-1], 0.5)
print('Synthetic 2s/5s/10s butterfly:', butterfly(4.0, 3.8, 3.5))
print(f'OU fit: mean={fit.mean:.3f}, theta/year={fit.theta:.3f}, sigma/sqrt(year)={fit.sigma:.3f}')
print(f'Half-life: {fit.half_life:.3f} years')
print(f'Six-month conditional mean={expected:.3f}; standard deviation={uncertainty:.3f}')
