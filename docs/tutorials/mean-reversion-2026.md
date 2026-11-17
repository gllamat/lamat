# A reproducible introduction to a rates butterfly and mean reversion

**Updated:** 17 November 2026. This is a new synthetic teaching example inspired by the [2018 MeanReversion tutorial](https://github.com/gllamat/MeanReversion/blob/master/notebooks/MeanReversionTutorial_1.ipynb). The historical notebook's data services are obsolete; its historical results are not reproduced here.

## 1. The question and data

A 2s/5s/10s butterfly summarizes the curvature of three rates: `-r2 + 2*r5 - r10`. Here each rate is expressed in **percent per annum**, so the result is in **percentage points**. This is a mathematical combination, not a duration-neutral position or a profit-and-loss series.

The [fixture](../../data/fixtures/synthetic-rates.json) contains three manually specified observations; it records its source, licence, units and revision and missing-value policies. It is synthetic, not historical Treasury data. On 19 January 2024 its values are 4.00%, 3.85% and 3.60%; the butterfly is `-4.00 + 2*3.85 - 3.60 = 0.10` percentage points, or 10 basis points. The date is an illustrative label, not a market observation.

## 2. The model

An Ornstein–Uhlenbeck (OU) process is written `dX = theta*(mu-X)*dt + sigma*dW`. The long-run mean is `mu`; positive `theta` sets the speed of reversion, and `sigma` sets random variation. For elapsed time `t`, conditional mean is `mu + (X0-mu)*exp(-theta*t)` and conditional variance is `sigma²*(1-exp(-2*theta*t))/(2*theta)`. The half-life of an expected deviation is `ln(2)/theta`.

Time in the example is measured in years: `theta` is per year and `sigma` is in the modelled variable's units per square root of a year. Consistent units are essential; these quantities change when the time unit changes. A half-life describes an average conditional decay under the model, not a guaranteed time to cross the mean.

## 3. Run the example

From the repository root, with Python 3.9 or newer:

```sh
PYTHONPATH=packages/quant-research/src python3 examples/mean_reversion.py
PYTHONPATH=packages/quant-research/src python3 -m unittest discover -s packages/quant-research/tests
```

The example prints the fixture's source and units and computes the most recent synthetic butterfly. Separately, it generates a seeded OU sequence using 520 weekly steps, with `dt=1/52` year, then fits and forecasts the simulated sequence. **The OU sequence is not the three fixture observations**, and the OU output is not fitted to market data or a trading strategy.

One run with seed 2026 produced a fitted mean of approximately -0.017, theta 2.426 per year, sigma 0.309 per square-root year, and half-life 0.286 years. The six-month conditional mean was 0.070 with standard deviation 0.134. Numerical output is rounded; exact random sequences may vary across Python implementations or versions.

## 4. Interpretation and limits

The calibrated model uses equally spaced data and an exact-transition autoregression with coefficient between zero and one. The small fixture checks the plumbing and arithmetic; it is too small for meaningful calibration. The simulated process demonstrates mechanics under a model chosen in advance. A good simulated fit does not establish that a real butterfly is stationary, or that any trading rule is profitable.

Before extending this to real research, identify a licensed provider, record data revisions and observation timing, define missing-day and day-count conventions, test model assumptions and parameter uncertainty, and use time-separated evaluation with explicit costs and risk. No live API or real-market performance claim is included.
