# Simultaneous events and expected log wealth

This small teaching example follows the idea of the historical [Kelly criterion article](https://www.linkedin.com/pulse/kelly-criterion-multiple-simultaneous-events-gerardo-lemus). The archived notebook enumerates binary outcomes and multiplies marginal probabilities, which assumes independent events. The example here instead accepts an explicit joint distribution, so dependence is visible in the input. It uses invented scenarios; it is not a forecast, investment recommendation or evidence of trading performance.

For event allocations `f_i` and scenario net returns `r_i`, ending wealth is `1 + sum(f_i * r_i)`; unallocated wealth remains at 1. Fractions are nonnegative, total allocation is at most one, and each net return is at least -1, excluding leveraged losses and short positions. Expected log wealth is the probability-weighted sum of `log(wealth)` over scenarios with positive probability. Wealth must be strictly positive in each such scenario. An impossible scenario with probability zero contributes nothing and does not rule out an allocation. The caller supplies a joint distribution whose probabilities sum to one; the code does not estimate probabilities or infer independence.

`grid_search` enumerates fractions in increments of `1 / steps` and excludes combinations that exhaust wealth in a possible scenario. It returns the best point on that finite grid, not a continuous optimum. A point-count cap makes the deliberately small search bounded. Scenario enumeration and the allocation grid both grow rapidly with the number of events; the method is not designed for large portfolios. Ties retain the first encountered feasible point. Costs, time horizons, changing probabilities, risk limits, leverage, estimation uncertainty and market impact are outside this model.

Run from the repository root:

```sh
PYTHONPATH=packages/quant-research/src python3 examples/kelly_scenarios.py
PYTHONPATH=packages/quant-research/src python3 -m unittest discover -s packages/quant-research/tests
```

The tests include the analytical single-event even-payoff solution with probability 0.75, a fair-game baseline, an explicit dependence comparison, zero-wealth and zero-probability boundaries, invalid inputs and the grid cap. The historical notebook, its data and its outputs were not executed or copied.
