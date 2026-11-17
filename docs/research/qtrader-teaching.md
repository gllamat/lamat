# QTrader: a tabular learning experiment on synthetic prices

This is a new teaching experiment informed by the historical [QTrader notebook](https://gist.github.com/gjlr2000/15da1e50cebf856cdcea9adfdd655d31/618effd3863a1d54c3c9653ecec4024907440ba3). The historical notebook used price and holdings as a discrete state and trained a tabular Q policy in a simulated mean-reverting market. It is not executed or reproduced here; neither original performance figures nor old external services are used.

## Model and timing

- **Environment:** seeded, bounded and tick-rounded synthetic mean-reverting marks. The clipped process is not an exact Ornstein–Uhlenbeck transition and is not a calibrated market model. Prices, ticks and costs are arbitrary linear units.
- **State:** a current price bin and current holding. The initial holding is flat; holdings are restricted to -1, 0 or 1 unit.
- **Actions:** select a target holding of -1, 0 or 1. After observing the current mark, the agent changes position at that mark; the new position earns the next mark change. A flip has two units of turnover. At the final mark the position is liquidated.
- **Reward:** position times the subsequent mark change, less a fixed cost per unit of turnover, including final liquidation. This is a linear P&L teaching reward; it is **not** the historical notebook's risk-adjusted reward or a Sharpe-ratio objective. No capital, return, financing, slippage beyond fixed costs, bid/ask model, impact, position margin, risk limit or stop-loss is modelled.
- **Learner:** Q-learning with an epsilon-greedy exploration rule and a fixed learning rate and discount. Terminal updates do not bootstrap; ties prefer the flat action. The state has no remaining-time feature, so the finite-horizon problem is only approximated. Training episodes are independently generated from one seeded random stream and always start at the centre and flat.
- **Evaluation:** after training, the Q table is frozen. Three policies see the same separately seeded held-out paths: the learned policy, always-flat and a fixed threshold that knows the simulated centre and tick. The threshold has privileged knowledge of the generator and is a benchmark, not a realistic market rule. Each episode starts and ends flat. The fixed seeds and parameters are specified before evaluation; no model selection is performed on held-out paths.

## Reproduce

From the repository root with Python 3.9 or later:

```sh
PYTHONPATH=packages/quant-research/src python3 examples/qtrader_teaching.py
PYTHONPATH=packages/quant-research/src python3 -m unittest discover -s packages/quant-research/tests
```

The example trains on 200 episodes from seed 7 and evaluates 50 separate episodes from seed 9001, reporting mean gross P&L, cost and net P&L for each policy. All paths are artificial and share the assumed process and parameters. A single seeded comparison is not a statistical validation; result magnitudes depend on the model, chosen assumptions and cost units. It is not evidence of returns, prediction accuracy or real-world viability. This model is a separate teaching baseline from the generic backtesting layer under development; an integration decision should follow both reviews.
