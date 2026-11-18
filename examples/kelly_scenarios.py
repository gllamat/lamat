"""Illustrative, invented even-payoff scenarios; not a trading recommendation."""
from lamat_quant.kelly import Scenario, expected_log_growth, grid_search

# Explicit joint probabilities: the two marginal win rates are .60 and .55.
# These numbers happen to describe independent events; no independence is assumed
# by the calculation, so a different joint distribution changes the answer.
outcomes = (
    Scenario(.33, (1., 1.)),
    Scenario(.27, (1., -1.)),
    Scenario(.22, (-1., 1.)),
    Scenario(.18, (-1., -1.)),
)
allocation, growth = grid_search(outcomes, steps=20)
print(f"Illustrative grid allocations: {allocation}")
print(f"Expected log growth under these invented assumptions: {growth:.6f}")
print(f"Unallocated baseline: {expected_log_growth(outcomes, (0., 0.)):.6f}")
