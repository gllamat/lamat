# Synthetic return distribution teaching

This independent example responds to the static review of the historical Black Crypto-Swans notebook in issue #54. It uses invented prices and does not reproduce historical market results or download data.

The return helper matches observations separated by exactly the requested elapsed time. It does not forward-fill gaps: missing endpoints produce no return. Timestamps are converted to UTC for matching, including across daylight-saving transitions. The example computes decimal log returns and passes those same returns to both the empirical cumulative distribution and normal Q-Q diagnostics. Duplicate observations in the ECDF are represented once at their cumulative probability.

The Q-Q reference normal distribution uses the sample mean and population standard deviation fitted to the same observations, with plotting positions `(i + 0.5) / n`. These descriptive diagnostics do not establish a normal distribution, estimate out-of-sample tail risk, model liquidation, or give trading advice. Overlapping horizons, selection bias, gaps, market microstructure and finite samples still need consideration. The historical notebook was not executed and its data, outputs and rights were not assessed by this example.

Run from the repository root:

```sh
PYTHONPATH=packages/quant-research/src python3 examples/return_distributions.py
PYTHONPATH=packages/quant-research/src python3 -m unittest discover -s packages/quant-research/tests
```
