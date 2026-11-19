"""Small, explicit-scenario Kelly teaching tools; not investment advice."""

from dataclasses import dataclass
import math
from typing import Iterable, Sequence, Tuple


@dataclass(frozen=True)
class Scenario:
    """Joint outcome probability and net return per unit allocated to each event."""

    probability: float
    returns: Tuple[float, ...]


def _validate_scenarios(scenarios: Iterable[Scenario]) -> Tuple[Scenario, ...]:
    scenarios = tuple(scenarios)
    if not scenarios or not scenarios[0].returns:
        raise ValueError("at least one scenario and one event are required")
    dimensions = len(scenarios[0].returns)
    for scenario in scenarios:
        if len(scenario.returns) != dimensions:
            raise ValueError("every scenario must cover the same events")
        if not math.isfinite(scenario.probability) or not 0 <= scenario.probability <= 1:
            raise ValueError("probabilities must be finite and between zero and one")
        if any(not math.isfinite(r) or r < -1 for r in scenario.returns):
            raise ValueError("returns must be finite and at least -1")
    if not math.isclose(math.fsum(s.probability for s in scenarios), 1.0, rel_tol=0, abs_tol=1e-12):
        raise ValueError("joint scenario probabilities must sum to one")
    return scenarios


def _validate_fractions(fractions: Sequence[float], dimensions: int) -> Tuple[float, ...]:
    fractions = tuple(fractions)
    if len(fractions) != dimensions or any(not math.isfinite(f) or f < 0 for f in fractions):
        raise ValueError("fractions must be finite, nonnegative and match the number of events")
    if math.fsum(fractions) > 1 + 1e-12:
        raise ValueError("total allocation cannot exceed one")
    return fractions


def _growth(scenarios: Sequence[Scenario], fractions: Sequence[float]) -> float:
    values = []
    for scenario in scenarios:
        if scenario.probability == 0:
            continue
        gain = math.fsum(f * r for f, r in zip(fractions, scenario.returns))
        if gain <= -1:
            raise ValueError("wealth must be positive in each possible scenario")
        values.append(scenario.probability * math.log1p(gain))
    return math.fsum(values)


def expected_log_growth(scenarios: Iterable[Scenario], fractions: Sequence[float]) -> float:
    """Return expected log wealth for explicit joint outcomes and allocations.

    Wealth is 1 + sum(fraction * net return); unused wealth remains uninvested.
    Zero-probability outcomes do not constrain wealth or contribute to the sum.
    """
    scenarios = _validate_scenarios(scenarios)
    fractions = _validate_fractions(fractions, len(scenarios[0].returns))
    return _growth(scenarios, fractions)


def _allocations(events: int, remaining: int, prefix: Tuple[int, ...] = ()):
    if events == 0:
        yield prefix
        return
    for count in range(remaining + 1):
        yield from _allocations(events - 1, remaining - count, prefix + (count,))


def grid_search(scenarios: Iterable[Scenario], steps: int = 20) -> Tuple[Tuple[float, ...], float]:
    """Find the best feasible grid point, not a continuous optimum.

    Fractions are nonnegative multiples of 1/steps, with total at most one.
    The point count is capped to keep this deliberately small example bounded.
    """
    scenarios = _validate_scenarios(scenarios)
    dimensions = len(scenarios[0].returns)
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1:
        raise ValueError("steps must be a positive integer")
    if dimensions > 8 or math.comb(steps + dimensions, dimensions) > 100_000:
        raise ValueError("grid is too large for this teaching example")
    best_fractions, best_growth = (0.0,) * dimensions, 0.0
    for allocation in _allocations(dimensions, steps):
        fractions = tuple(n / steps for n in allocation)
        try:
            growth = _growth(scenarios, fractions)
        except ValueError:  # Reject grid points that can exhaust wealth.
            continue
        if growth > best_growth:
            best_fractions, best_growth = fractions, growth
    return best_fractions, best_growth
