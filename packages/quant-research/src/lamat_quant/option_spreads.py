"""Synthetic European call-spread teaching; no market-data access."""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class StrikeInterval:
    lower_strike: float
    upper_strike: float
    call_spread: float
    average_survival: float


def interval_survival(strikes, calls, discount_factor):
    """Return strike-interval averages of risk-neutral survival probabilities.

    Calls are European, on the same underlying and expiry, in the same currency
    and per-unit scale as strikes. The positive discount factor is supplied by
    the caller. This finite grid does not identify a full distribution.
    """
    try:
        k = tuple(float(v) for v in strikes)
        c = tuple(float(v) for v in calls)
        discount = float(discount_factor)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError('inputs must be finite numbers') from exc
    if (len(k) != len(c) or len(k) < 2 or not math.isfinite(discount)
            or discount <= 0 or not all(math.isfinite(v) for v in k + c)):
        raise ValueError('invalid grid, prices or discount factor')
    if any(v < 0 for v in k + c) or any(b <= a for a, b in zip(k, k[1:])):
        raise ValueError('strikes must increase strictly and inputs be nonnegative')
    rows = []
    for left, right, first, second in zip(k, k[1:], c, c[1:]):
        width = right - left
        spread = first - second
        denominator = discount * width
        if not math.isfinite(width) or not math.isfinite(spread) or not math.isfinite(denominator) or denominator <= 0:
            raise ValueError('strike interval or discounted width is not finite')
        average = spread / denominator
        if not math.isfinite(average) or average < -1e-12 or average > 1 + 1e-12:
            raise ValueError('call spread outside discounted no-arbitrage bounds')
        rows.append(StrikeInterval(left, right, spread, average))
    if any(b.average_survival > a.average_survival + 1e-12 for a, b in zip(rows, rows[1:])):
        raise ValueError('call prices are not convex across unequal strike intervals')
    return tuple(rows)
