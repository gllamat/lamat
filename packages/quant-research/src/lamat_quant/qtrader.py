"""A small tabular Q-learning teaching experiment using synthetic prices only.

A state observes a discretized current price and current position. An action
chooses a target position. The action trades at the current observed mark,
then that position earns the next mark change. Costs are per unit of turnover.
"""
from dataclasses import dataclass
import math
import random

POSITIONS = (-1, 0, 1)


@dataclass(frozen=True)
class Config:
    centre: float = 10.0
    tick: float = 0.5
    reversion: float = 0.2
    volatility: float = 0.7
    cost: float = 0.05
    lower: float = 1.0
    upper: float = 19.0

    def __post_init__(self):
        if not all(math.isfinite(v) for v in (self.centre, self.tick, self.reversion, self.volatility, self.cost, self.lower, self.upper)):
            raise ValueError('configuration must be finite')
        if not (0 < self.lower < self.centre < self.upper and self.tick > 0 and 0 < self.reversion < 1 and self.volatility > 0 and self.cost >= 0):
            raise ValueError('invalid bounds, process parameters or costs')


def generate_path(cfg, steps, rng):
    """A bounded discretized mean-reverting toy process, not a market model."""
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1:
        raise ValueError('steps must be a positive integer')
    values = [cfg.centre]
    for _ in range(steps):
        current = values[-1]
        nxt = current + cfg.reversion * (cfg.centre - current) + rng.gauss(0, cfg.volatility)
        # Round to a price grid relative to centre, then clip to bounds.
        nxt = cfg.centre + round((nxt - cfg.centre) / cfg.tick) * cfg.tick
        values.append(min(cfg.upper, max(cfg.lower, nxt)))
    return tuple(values)


def state(price, holding, cfg):
    if not math.isfinite(price) or price < cfg.lower or price > cfg.upper or holding not in POSITIONS:
        raise ValueError('invalid price or holding')
    return (round((price - cfg.centre) / cfg.tick), holding)


def transition(price, holding, target, next_price, cfg, terminal=False):
    """Trade at price, earn next change, and pay terminal liquidation cost."""
    state(price, holding, cfg)
    state(next_price, target, cfg)
    if target not in POSITIONS:
        raise ValueError('invalid target position')
    pnl = target * (next_price - price)
    turnover = abs(target - holding) + (abs(target) if terminal else 0)
    cost = cfg.cost * turnover
    return (0 if terminal else target), pnl, cost, pnl - cost


def greedy_action(table, key):
    """Choose flat on ties to avoid arbitrary exposure in unseen states."""
    values = table.get(key, (0.0, 0.0, 0.0))
    return max((1, 0, 2), key=lambda i: values[i])


def train(cfg, *, episodes=200, steps=200, seed=7, alpha=0.1, gamma=0.9, epsilon=0.2):
    if isinstance(episodes, bool) or not isinstance(episodes, int) or episodes < 1:
        raise ValueError('episodes must be a positive integer')
    if not all(math.isfinite(x) for x in (alpha, gamma, epsilon)) or not (0 < alpha <= 1 and 0 <= gamma <= 1 and 0 <= epsilon <= 1):
        raise ValueError('invalid learning parameters')
    rng = random.Random(seed)
    table = {}
    for _ in range(episodes):
        path = generate_path(cfg, steps, rng)
        holding = 0
        for t in range(steps):
            key = state(path[t], holding, cfg)
            action_index = rng.randrange(3) if rng.random() < epsilon else greedy_action(table, key)
            action = POSITIONS[action_index]
            terminal = t == steps - 1
            next_holding, _, _, reward = transition(path[t], holding, action, path[t + 1], cfg, terminal)
            next_key = state(path[t + 1], next_holding, cfg)
            future = 0.0 if terminal else max(table.get(next_key, (0.0, 0.0, 0.0)))
            q = table.setdefault(key, [0.0, 0.0, 0.0])
            q[action_index] += alpha * (reward + gamma * future - q[action_index])
            holding = next_holding
    return {key: tuple(values) for key, values in table.items()}


def evaluate(cfg, table, *, episodes=50, steps=200, seed=9001, policy='learned'):
    """Evaluate frozen learned, flat or fixed threshold policies on new paths."""
    if isinstance(episodes, bool) or not isinstance(episodes, int) or episodes < 1:
        raise ValueError('episodes must be a positive integer')
    if policy not in ('learned', 'flat', 'threshold'):
        raise ValueError('unknown policy')
    rng = random.Random(seed)
    totals = []
    for _ in range(episodes):
        path = generate_path(cfg, steps, rng)
        holding = 0
        gross_total = cost_total = 0.0
        for t in range(steps):
            if policy == 'flat':
                target = 0
            elif policy == 'threshold':
                target = 1 if path[t] <= cfg.centre - cfg.tick else (-1 if path[t] >= cfg.centre + cfg.tick else 0)
            else:
                target = POSITIONS[greedy_action(table, state(path[t], holding, cfg))]
            holding, gross, cost, _ = transition(path[t], holding, target, path[t + 1], cfg, t == steps - 1)
            gross_total += gross
            cost_total += cost
        totals.append((gross_total, cost_total, gross_total - cost_total))
    return tuple(totals)
