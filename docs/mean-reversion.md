# Mean reversion: a reproducible starting point

The original [Lamat mean-reversion tutorial](https://github.com/gllamat/MeanReversion/blob/master/notebooks/MeanReversionTutorial_1.ipynb) uses a 2s/5s/10s Treasury butterfly to introduce an Ornstein–Uhlenbeck (OU) model. This first modernization extracts the butterfly, conditional forecast, half-life and calibration into reusable Python functions. It uses **synthetic data only**; it does not claim an updated market result.

For `dX = theta (mu - X) dt + sigma dW`, the conditional mean is `mu + (x - mu) exp(-theta t)` and conditional variance is `sigma² (1 - exp(-2 theta t)) / (2 theta)`. The example expresses `t` in years, `theta` per year and `sigma` per square root of a year. The estimator fits the exact Gaussian transition by conditional least squares at equally spaced times. It rejects coefficients outside (0, 1); that rejection is not a stationarity test, and a successful fit does not establish a trading opportunity.

Next work: a licensed, documented data adapter; missing-day and calendar handling; uncertainty estimates; stationarity and cointegration tests; and a realistic out-of-sample study with explicit costs. Rates and simulated outcomes are illustrative, not investment advice or evidence of returns.
