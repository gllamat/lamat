"""Ornstein-Uhlenbeck model for evenly spaced observations.

Time is expressed in one consistent unit throughout: theta is per unit of
``dt`` and sigma is per square root of that unit. No trading P&L is implied.
"""
from dataclasses import dataclass
import math
from typing import Iterable, Sequence


@dataclass(frozen=True)
class OUParameters:
    mean: float
    theta: float
    sigma: float

    def __post_init__(self):
        if not all(math.isfinite(x) for x in (self.mean, self.theta, self.sigma)):
            raise ValueError("parameters must be finite")
        if self.theta <= 0 or self.sigma < 0:
            raise ValueError("theta must be positive and sigma non-negative")

    @property
    def half_life(self) -> float:
        return math.log(2) / self.theta

    @property
    def stationary_std(self) -> float:
        return self.sigma / math.sqrt(2 * self.theta)

    def forecast(self, current: float, horizon: float) -> tuple:
        """Conditional expectation and standard deviation at ``horizon``."""
        if not math.isfinite(current) or not math.isfinite(horizon) or horizon < 0:
            raise ValueError("current and non-negative horizon must be finite")
        decay = math.exp(-self.theta * horizon)
        variance = self.sigma ** 2 * (-math.expm1(-2 * self.theta * horizon)) / (2 * self.theta)
        return self.mean + (current - self.mean) * decay, math.sqrt(variance)


def butterfly(two_year: float, five_year: float, ten_year: float) -> float:
    """Return -2y + 2*5y - 10y, using the input's rate units."""
    if not all(math.isfinite(x) for x in (two_year, five_year, ten_year)):
        raise ValueError("rates must be finite")
    return -two_year + 2 * five_year - ten_year


def fit_ou(values: Iterable[float], dt: float) -> OUParameters:
    """Fit an OU process through its exact Gaussian AR(1) transition.

    Observations must be equally spaced by ``dt``. The OLS conditional fit
    requires 0 < autoregressive coefficient < 1; other estimates are rejected
    rather than presented as evidence of mean reversion. Not a stationarity test.
    """
    data = [float(x) for x in values]
    if not math.isfinite(dt) or dt <= 0 or len(data) < 4:
        raise ValueError("need at least four observations and positive finite dt")
    if not all(math.isfinite(x) for x in data):
        raise ValueError("observations must be finite")
    x, y = data[:-1], data[1:]
    xbar, ybar = sum(x) / len(x), sum(y) / len(y)
    denominator = sum((v - xbar) ** 2 for v in x)
    if denominator == 0:
        raise ValueError("cannot fit a constant series")
    phi = sum((a - xbar) * (b - ybar) for a, b in zip(x, y)) / denominator
    if not 0 < phi < 1:
        raise ValueError("fitted AR coefficient must be between zero and one")
    intercept = ybar - phi * xbar
    mean = intercept / (1 - phi)
    theta = -math.log(phi) / dt
    residual_variance = sum((b - intercept - phi * a) ** 2 for a, b in zip(x, y)) / len(x)
    sigma = math.sqrt(residual_variance * 2 * theta / (-math.expm1(-2 * theta * dt)))
    return OUParameters(mean, theta, sigma)
