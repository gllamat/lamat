# Synthetic option-spread teaching

The historical crypto-options notebook motivated this separate example (#62). It uses invented European call prices, no historical data or exchange connection, and no original outputs. It is a numerical lesson, not trading advice or a forecast.

For a deterministic positive discount factor `D`, a European call with strike `K` has price `C(K) = D E[(S_T - K)+]` under a suitable risk-neutral pricing measure. The adjacent call spread `(C(a) - C(b)) / (D (b - a))` is the average survival probability over the entire strike interval `[a, b]`. It is not necessarily the survival probability at the midpoint. The input calls and strikes must use compatible currency and per-unit scales, and the same underlying and expiry.

Unequal strike gaps require separately normalized adjacent spreads. The historical notebook's unweighted second difference is not a reliable convexity test on an uneven grid: for strikes `90, 100, 120` and calls `16, 9, 1`, the adjacent slopes are `-0.7, -0.4`, whereas the unweighted second difference is negative. The example validates decreasing, convex call prices through their normalized spreads and rejects simple violations; it does not establish all possible no-arbitrage constraints or clean actual quotes.

The finite strike grid does not determine either tail or a complete distribution. The values are model-dependent risk-neutral quantities, not real-world event probabilities, and can be affected by spreads, stale prices, liquidity, units, discounting and data quality. See [the Federal Reserve Bank of San Francisco's discussion of option-implied probabilities](https://www.frbsf.org/research-and-insights/publications/economic-letter/2014/05/financial-market-outlook-inflation-derivatives/).

From the repository root:

```sh
PYTHONPATH=packages/quant-research/src python examples/option_spread_teaching.py
PYTHONPATH=packages/quant-research/src python -m unittest discover -s packages/quant-research/tests
```
