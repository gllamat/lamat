# Synthetic rates forecast evaluation

This independent teaching example responds to the historical rates LSTM audit in #54 and #60. It uses a rolling mean as a transparent baseline, not an LSTM, and uses invented values rather than historical data, notebook outputs or credentials. The result is not evidence of market forecasting performance or financial advice.

From the repository root, run:

```sh
PYTHONPATH=packages/quant-research/src python examples/rates_forecast_evaluation.py
PYTHONPATH=packages/quant-research/src python -m unittest discover -s packages/quant-research/tests
```

The initial origin is the last training observation. A forecast's target index is its origin plus the specified horizon; the evaluation joins each prediction to the actual at that exact index. At later origins it uses observations available through that origin. This rolling-origin exercise is different from producing every prediction once at the initial origin. Horizons count observations, not calendar days. Min/max scaling is fitted once to the training slice and frozen; held-out observations may lie outside the training range. The rolling-mean baseline is affine-invariant, so scaling does not change its prediction: it is included to expose the train-only boundary, not to imply scaling improves this baseline.

The synthetic series is deterministic and intentionally simple. There is no data-vintage model, missing-data treatment, statistical uncertainty, transaction cost, model selection, neural network, or performance validation on real rates. A real study requires authorized point-in-time data, a carefully selected evaluation protocol and additional baselines; do not infer results for the original notebook from this example.
