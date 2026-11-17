"""Small, auditable linear-mark backtests; this is not a brokerage simulator.

A signal observes the current close. It trades after that close and is first
exposed to the next close-to-close change. Costs are absolute currency units per
unit traded (not a percentage of price); marks and costs must share units.
"""
from dataclasses import dataclass
import math
import random
from typing import Iterable, Tuple

from .mean_reversion import OUParameters


@dataclass(frozen=True)
class ThresholdRule:
    """Enter outside centre +/- entry; exit at centre +/- exit, no same-bar flip."""
    centre: float
    entry: float
    exit: float = 0.0
    size: float = 1.0

    def __post_init__(self):
        if not all(math.isfinite(x) for x in (self.centre, self.entry, self.exit, self.size)):
            raise ValueError('rule values must be finite')
        if not (self.entry > 0 and 0 <= self.exit < self.entry and self.size > 0):
            raise ValueError('require entry > exit >= 0 and size > 0')

    def position(self, mark: float, current: float) -> float:
        if current > 0:
            return 0.0 if mark >= self.centre - self.exit else current
        if current < 0:
            return 0.0 if mark <= self.centre + self.exit else current
        if mark <= self.centre - self.entry:
            return self.size
        if mark >= self.centre + self.entry:
            return -self.size
        return 0.0


@dataclass(frozen=True)
class BacktestRow:
    index: int
    mark: float
    position_before: float
    position_after: float
    gross_pnl: float
    trade_cost: float
    net_pnl: float
    cumulative_net_pnl: float


@dataclass(frozen=True)
class BacktestResult:
    rows: Tuple[BacktestRow, ...]
    gross_pnl: float
    costs: float
    net_pnl: float


def simulate_ou(params: OUParameters, initial: float, dt: float, steps: int, seed: int) -> Tuple[float, ...]:
    """Return initial mark plus ``steps`` exact-transition simulated marks."""
    if not math.isfinite(initial) or not math.isfinite(dt) or dt <= 0:
        raise ValueError('initial and positive dt must be finite')
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1:
        raise ValueError('steps must be a positive integer')
    rng = random.Random(seed)
    marks = [float(initial)]
    for _ in range(steps):
        mean, std = params.forecast(marks[-1], dt)
        marks.append(rng.gauss(mean, std))
    return tuple(marks)


def run_backtest(marks: Iterable[float], rule: ThresholdRule, cost_per_unit: float) -> BacktestResult:
    """Trade after each observation, mark existing position first, close at end.

    Input order is chronological. Starting and terminal positions are flat.
    The terminal close pays a cost; no new signal is taken at the final mark.
    Costs are charged on absolute position turnover, including opening and exit.
    """
    values = tuple(float(x) for x in marks)
    if len(values) < 2 or not all(math.isfinite(x) for x in values):
        raise ValueError('at least two finite marks are required')
    if not math.isfinite(cost_per_unit) or cost_per_unit < 0:
        raise ValueError('cost must be finite and non-negative')
    position = gross_total = cost_total = net_total = 0.0
    rows = []
    for i, mark in enumerate(values):
        before = position
        gross = before * (mark - values[i - 1]) if i else 0.0
        position = 0.0 if i == len(values) - 1 else rule.position(mark, before)
        cost = abs(position - before) * cost_per_unit
        net = gross - cost
        gross_total += gross
        cost_total += cost
        net_total += net
        rows.append(BacktestRow(i, mark, before, position, gross, cost, net, net_total))
    return BacktestResult(tuple(rows), gross_total, cost_total, net_total)


def evaluate_chronologically(marks: Iterable[float], split_index: int, rule: ThresholdRule,
                             cost_per_unit: float) -> Tuple[BacktestResult, BacktestResult]:
    """Evaluate two non-overlapping segments, flat at each boundary.

    ``split_index`` is the first test observation. Rule parameters are fixed by
    the caller before evaluation; this helper performs no optimisation or fit.
    No return across the split is earned and no position carries into test.
    """
    values = tuple(marks)
    if isinstance(split_index, bool) or not isinstance(split_index, int):
        raise ValueError('split_index must be an integer')
    if split_index < 2 or len(values) - split_index < 2:
        raise ValueError('each segment requires at least two observations')
    return (run_backtest(values[:split_index], rule, cost_per_unit),
            run_backtest(values[split_index:], rule, cost_per_unit))
