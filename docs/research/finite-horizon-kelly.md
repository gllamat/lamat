# Finite-horizon outcomes and Kelly sizing

A stop-hit probability alone does not specify the return from a trade. For a finite horizon, the upper and lower barriers may both remain unhit, and a strategy must define the resulting payoff. An upper-hit and a lower-hit probability also cannot be treated as mutually exclusive if each merely means the barrier was touched at any time. These choices affect sizing.

This independent teaching example defines three **mutually exclusive** synthetic outcomes: upper barrier first (probability 0.4, net return +1 per unit allocated), lower barrier first (0.2, net return -1), and neither barrier reached by the horizon (0.4, net return 0). It assumes no costs, constant probabilities, and an uninvested remainder earning zero. Each scenario's wealth is `1 + fraction × return`; strictly positive wealth is required in every positive-probability scenario. Actual stop execution, simultaneous hits, market gaps and the value of an open position at the horizon can produce different payoffs. No probabilities or data are inferred from a historical simulation.

For a fraction `f` in the feasible long-only range, expected log growth is

`0.4 log(1 + f) + 0.2 log(1 - f) + 0.4 log(1)`.

Its derivative vanishes at `(0.4 - 0.2) / (0.4 + 0.2) = 1/3`; concavity makes this the maximum. In contrast, inserting the **unconditional** upper-hit probability into the equal-odds binary shortcut `2p - 1` yields -0.2, despite the positive optimum in this specified example. The binary shortcut assumes win and loss are exhaustive with the specified payoff, which these three unconditional outcomes are not. Conditional on a non-flat outcome, the win probability is 2/3, and the shortcut agrees here because flat wealth is unchanged. This agreement does not generalize to a nonzero no-hit payoff or unequal win/loss magnitudes.

Run:

```sh
PYTHONPATH=packages/quant-research/src python3 examples/finite_horizon_kelly.py
```

The grid search evaluates only multiples of 1/30 and happens to include 1/3. A different grid need not find the continuous optimum. This is a mathematical illustration, not a trading strategy, performance claim or investment advice. Probability estimates, costs, drawdowns, dependence between repeated outcomes, and model uncertainty are outside its scope.
