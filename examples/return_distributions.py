"""Inspect synthetic log returns; no historical market data or network access."""
from datetime import datetime, timedelta, timezone
from lamat_quant.return_distributions import elapsed_log_returns, distribution_points

start = datetime(2026, 1, 1, tzinfo=timezone.utc)
prices = [100, 101, 100, 99, 105, 104, 106]
observations = [(start + timedelta(minutes=i), price) for i, price in enumerate(prices)]
returns = elapsed_log_returns(observations, timedelta(minutes=1))
points = distribution_points([r.log_return for r in returns])
print('Synthetic one-minute log returns:', [round(r.log_return, 4) for r in returns])
print('ECDF (return, cumulative fraction):', points['ecdf'])
print('Q-Q (fitted normal quantile, observed return):', points['qq'])
print('The fitted distribution describes this sample; it is not a tail-risk forecast.')
