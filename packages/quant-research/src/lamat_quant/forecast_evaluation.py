"""Small, chronological synthetic forecasting lesson, not a market model."""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Forecast:
    origin: int
    target: int
    horizon: int
    prediction: float
    actual: float


@dataclass(frozen=True)
class Evaluation:
    train_min: float
    train_max: float
    forecasts: tuple


def evaluate_rolling_mean(values, train_end, lookback, horizon):
    """Freeze scaling on values[:train_end], then forecast using observed history.

    Indices are observation positions, not calendar days. The initial forecast
    originates at train_end - 1; later origins incorporate newly observed data.
    This is a rolling-origin evaluation, not a fixed-origin multi-step forecast.
    """
    if any(isinstance(x, bool) or not isinstance(x, int) for x in (train_end, lookback, horizon)):
        raise ValueError('split, lookback and horizon must be integers')
    if lookback < 1 or horizon < 1 or train_end < lookback:
        raise ValueError('invalid lookback, horizon or training split')
    try:
        data = tuple(float(v) for v in values)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError('values must be finite numbers') from exc
    if not all(math.isfinite(v) for v in data):
        raise ValueError('values must be finite numbers')
    if train_end >= len(data) or train_end - 1 + horizon >= len(data):
        raise ValueError('not enough held-out observations for this horizon')
    low, high = min(data[:train_end]), max(data[:train_end])
    scale = high - low if high > low else 1.0
    forecasts = []
    for origin in range(train_end - 1, len(data) - horizon):
        observed = data[origin - lookback + 1:origin + 1]
        scaled_mean = sum((v - low) / scale for v in observed) / lookback
        target = origin + horizon
        forecasts.append(Forecast(origin, target, horizon,
                                  low + scale * scaled_mean, data[target]))
    return Evaluation(low, high, tuple(forecasts))
