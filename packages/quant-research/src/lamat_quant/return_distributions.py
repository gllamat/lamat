"""Elapsed-time returns and descriptive distribution diagnostics.

Educational utilities, not a market-risk or liquidation model.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import math
from statistics import NormalDist, fmean, pstdev


@dataclass(frozen=True)
class TimedReturn:
    start: datetime
    end: datetime
    log_return: float


def elapsed_log_returns(observations, horizon):
    """Return log returns only where both exact timestamps are observed.

    Observations are (timezone-aware datetime, positive price) pairs in strictly
    increasing order. Gaps are not filled or treated as adjacent time periods.
    Returns are decimal log returns, not percentages.
    """
    if not isinstance(horizon, timedelta) or horizon <= timedelta(0):
        raise ValueError('horizon must be a positive timedelta')
    prices = {}
    previous = None
    results = []
    for timestamp, raw_price in observations:
        if not isinstance(timestamp, datetime) or timestamp.utcoffset() is None:
            raise ValueError('timestamps must be timezone-aware datetimes')
        instant = timestamp.astimezone(timezone.utc)
        if previous is not None and instant <= previous:
            raise ValueError('timestamps must be strictly increasing')
        try:
            price = float(raw_price)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError('prices must be finite and positive') from exc
        if not math.isfinite(price) or price <= 0:
            raise ValueError('prices must be finite and positive')
        start = instant - horizon
        if start in prices:
            # Difference of logs avoids overflow from dividing extreme prices.
            value = math.log(price) - math.log(prices[start][1])
            results.append(TimedReturn(prices[start][0], timestamp, value))
        prices[instant] = (timestamp, price)
        previous = instant
    return tuple(results)


def distribution_points(values):
    """Describe a sample and return empirical CDF and normal Q-Q points.

    Normal quantiles use mean and population standard deviation fitted to this
    same sample, so these descriptive plots are not out-of-sample risk estimates.
    Each Q-Q pair is (fitted-normal quantile, observed value).
    """
    try:
        sample = sorted(float(v) for v in values)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError('sample must contain finite numbers') from exc
    if len(sample) < 2 or not all(math.isfinite(v) for v in sample):
        raise ValueError('sample must contain at least two finite numbers')
    mean, std = fmean(sample), pstdev(sample)
    if not math.isfinite(mean) or not math.isfinite(std) or std <= 0:
        raise ValueError('sample must have finite, nonzero variation')
    normal = NormalDist(mean, std)
    count = len(sample)
    return {
        'mean': mean,
        'std': std,
        'ecdf': tuple((x, (i + 1) / count) for i, x in enumerate(sample)
                      if i == count - 1 or x != sample[i + 1]),
        'qq': tuple((normal.inv_cdf((i + .5) / count), x) for i, x in enumerate(sample)),
    }
