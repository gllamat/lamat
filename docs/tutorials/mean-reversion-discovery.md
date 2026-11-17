# Mean-reversion discovery: synthetic comparison

This dated example revisits the questions in the [historical second tutorial](https://github.com/gllamat/MeanReversion/blob/master/notebooks/MeanReversionTutorial_2.ipynb) with **synthetic data only**. It does not reproduce the historical results or use obsolete services. Three synthetic series share a simulated random-walk factor and each has independent stationary AR noise. This construction deliberately creates cointegration; finding it here checks the example's mechanics, not predictive skill in markets.

## Reproduce

Python 3.9+ and a network connection for installation are required. The original standard-library example remains independent of these optional scientific packages.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r packages/quant-research/requirements-statistics.txt
PYTHONPATH=packages/quant-research/src .venv/bin/python examples/mean_reversion_discovery.py
PYTHONPATH=packages/quant-research/src .venv/bin/python -m unittest discover -s packages/quant-research/statistics-tests
```

The requirements constrain versions but are not a lockfile; exact transitive versions and numerical outputs may differ across platforms or future installs. GitHub Actions exercises Python 3.9 and 3.13. Data are generated locally with NumPy's seed 42; the first 600 observations are training, and the next 200 are held out. OLS pair coefficients and PCA directions use the training slice only. The held-out spread uses the frozen training coefficients; its ADF is descriptive rather than a prospective trading test.

## What each method says

- **Hurst-style variance scaling:** estimates half the log–log slope of increment variance over lags 2, 4, 8, 16 and 32. It is a scale-dependent heuristic, not a stationarity test. Finite samples, nonstationarity and the selected lags change the estimate. The implementation is intentionally identified by its estimator, not treated as interchangeable with other Hurst methods.
- **ADF:** tests the null of a unit root with a constant and AIC lag selection. Failure to reject does not prove a unit root; rejection is not proof that a model is stable, mean-reverting in a useful way or profitable. The ordinary ADF p-value applied to an in-sample fitted pair residual has the wrong reference distribution for testing cointegration and is shown only as a descriptive statistic.
- **Pairs and Engle–Granger:** a training OLS regression with intercept defines the pair's hedge ratio. The Engle–Granger test uses its appropriate residual-based p-value for the null of no cointegration. Its standard interpretation assumes integrated series and appropriate specification. Selection of pairs, structural breaks and multiple testing are not addressed.
- **PCA:** centred, unscaled level PCA gives orthogonal directions ordered by explained variance. All three synthetic series use the same units; different scales would alter the result. A low-variance component need not be stationary or cointegrating, and PCA signs are arbitrary.
- **Johansen:** the trace test reports statistics and 95% critical values for successive rank hypotheses using `det_order=0` and one lagged difference. Deterministic terms and lag choice matter. The example reports values rather than declaring an automatically selected rank; results are in-sample and may change with the sample.

No transaction costs, execution rules, data revisions, parameter uncertainty, multiple-testing adjustment or out-of-sample performance are modelled. Real data require licensing, time alignment, realistic look-ahead controls and independent evaluation before use.
