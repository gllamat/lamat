# Task 11: simulation and backtesting — review record

**Board task:** [Build a transparent simulation and backtesting layer](https://github.com/gllamat/lamat/issues/11).

## Deliverable

The [simulation and backtest module](../../packages/quant-research/src/lamat_quant/backtest.py) provides an exact-transition, seeded OU simulation; a fixed threshold entry/exit rule; bar-by-bar positions, gross P&L, transaction costs and net P&L; and a two-segment chronological evaluation helper. The [standalone example](../../examples/simulation_backtest.py) generates synthetic marks and runs a fixed rule across two disjoint segments. No external data or dependencies are needed.

For a mark observed at time `t`, the previous position earns the change from `t-1` to `t`; only then is the signal evaluated and the position changed. The new position earns its first mark change in the next period. Each segment starts flat and is liquidated at its final mark, with transaction costs on all opening and closing turnover. The split is the first test observation: no return across the split is earned. Rule parameters are supplied by the caller and are not fitted or selected by this example.

Marks are **linear units**, and P&L is position times mark change. A cost is a fixed amount per unit traded, in the same monetary units as the mark; it is not a percentage, basis points, bid/ask model or annualized return. Negative synthetic marks are permitted. Thresholds and costs are illustrative and not comparable to a specified traded contract without a contract multiplier and unit convention.

## Reproduce and verify

From the repository root, with Python 3.9 or newer:

```sh
PYTHONPATH=packages/quant-research/src python3 examples/simulation_backtest.py
PYTHONPATH=packages/quant-research/src python3 -m unittest discover -s packages/quant-research/tests
```

The seed-2026 example prints 400 and 201 observations and deterministic gross, cost and net figures. The values describe only one synthetic path. Tests check analytically worked long/short trades, position flips, opening and closing costs, boundary liquidation, segmentation, invalid inputs, deterministic seeds and the absence of pre-entry/future-mark influence on earlier rows.

## Limitations for human review

The simulator assumes exact execution at observed marks with a fixed cost. There are no timestamps, calendars, funding, borrow, leverage, contract multipliers, risk controls, capital constraints, slippage or market impact. Marks must already be in chronological order; no sorting, missing-date detection or point-in-time data checks are performed. The OU process and fixed parameters are a synthetic demonstration, not evidence of stationarity, market behaviour or profitable performance. The caller is responsible for selecting/fitting rules using only appropriate training data, and for any independent out-of-sample or walk-forward evaluation; this helper does not optimize parameters or prevent a caller from fitting on future data before calling it.

**Human review:** inspect timing, the example and tests, choose meaningful market units and cost assumptions before applying to real data, and review the pull request and checks.
