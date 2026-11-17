"""Small neural Q-function comparison for the synthetic QTrader environment.

This is an online, one-step semi-gradient learner with a periodically frozen
 target network; it is an educational experiment, not a market model.
"""
import math
import random

from .qtrader import POSITIONS, generate_path, state, transition


class Network:
    """One tanh hidden layer; all operations use the Python standard library."""
    def __init__(self, rng, hidden=8):
        self.w1 = [[rng.uniform(-.3, .3) for _ in range(2)] for _ in range(hidden)]
        self.b1 = [0.0] * hidden
        self.w2 = [[rng.uniform(-.3, .3) for _ in range(hidden)] for _ in POSITIONS]
        self.b2 = [0.0] * len(POSITIONS)

    def copy(self):
        other = object.__new__(Network)
        other.w1 = [row[:] for row in self.w1]
        other.b1 = self.b1[:]
        other.w2 = [row[:] for row in self.w2]
        other.b2 = self.b2[:]
        return other

    def values(self, x):
        hidden = [math.tanh(sum(w * v for w, v in zip(row, x)) + b)
                  for row, b in zip(self.w1, self.b1)]
        return tuple(sum(w * h for w, h in zip(row, hidden)) + b
                     for row, b in zip(self.w2, self.b2))

    def update(self, x, action, target, rate):
        """Update only the selected output against a fixed one-step target."""
        hidden = [math.tanh(sum(w * v for w, v in zip(row, x)) + b)
                  for row, b in zip(self.w1, self.b1)]
        prediction = sum(w * h for w, h in zip(self.w2[action], hidden)) + self.b2[action]
        error = max(-5.0, min(5.0, target - prediction))
        old_output = self.w2[action][:]
        for j, h in enumerate(hidden):
            self.w2[action][j] += rate * error * h
            delta = error * old_output[j] * (1 - h * h)
            for k in range(2):
                self.w1[j][k] += rate * delta * x[k]
            self.b1[j] += rate * delta
        self.b2[action] += rate * error


def features(price, holding, cfg):
    state(price, holding, cfg)  # reuse the baseline's input validation
    return ((price - cfg.centre) / (cfg.upper - cfg.lower), float(holding))


def action_index(values):
    return max((1, 0, 2), key=lambda i: values[i])


def train_neural(cfg, *, episodes=200, steps=200, seed=7, rate=.005,
                 gamma=.9, epsilon=.2, target_interval=100):
    if isinstance(episodes, bool) or not isinstance(episodes, int) or episodes < 1:
        raise ValueError('episodes must be a positive integer')
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1:
        raise ValueError('steps must be a positive integer')
    if isinstance(target_interval, bool) or not isinstance(target_interval, int) or target_interval < 1:
        raise ValueError('target_interval must be a positive integer')
    if not all(math.isfinite(x) for x in (rate, gamma, epsilon)) or not (0 < rate <= 1 and 0 <= gamma <= 1 and 0 <= epsilon <= 1):
        raise ValueError('invalid learning parameters')
    # Separate streams ensure the price sequence does not depend on action draws.
    path_rng = random.Random(seed)
    action_rng = random.Random(seed + 1)
    model = Network(random.Random(seed + 2))
    target_net = model.copy()
    updates = 0
    for _ in range(episodes):
        path = generate_path(cfg, steps, path_rng)
        holding = 0
        for t in range(steps):
            x = features(path[t], holding, cfg)
            idx = action_rng.randrange(3) if action_rng.random() < epsilon else action_index(model.values(x))
            terminal = t == steps - 1
            next_holding, _, _, reward = transition(path[t], holding, POSITIONS[idx], path[t + 1], cfg, terminal)
            future = 0.0 if terminal else max(target_net.values(features(path[t + 1], next_holding, cfg)))
            model.update(x, idx, reward + gamma * future, rate)
            updates += 1
            if updates % target_interval == 0:
                target_net = model.copy()
            holding = next_holding
    return model


def evaluate_neural(cfg, model, *, episodes=50, steps=200, seed=9001):
    """Evaluate frozen weights on the exact paths used by tabular evaluate."""
    if isinstance(episodes, bool) or not isinstance(episodes, int) or episodes < 1:
        raise ValueError('episodes must be a positive integer')
    rng = random.Random(seed)
    totals = []
    for _ in range(episodes):
        path = generate_path(cfg, steps, rng)
        holding = 0
        gross_total = cost_total = 0.0
        for t in range(steps):
            idx = action_index(model.values(features(path[t], holding, cfg)))
            holding, gross, cost, _ = transition(path[t], holding, POSITIONS[idx], path[t + 1], cfg, t == steps - 1)
            gross_total += gross
            cost_total += cost
        totals.append((gross_total, cost_total, gross_total - cost_total))
    return tuple(totals)
