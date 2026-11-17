"""Synthetic diagnostics for persistence and cointegration.

These methods describe a supplied sample; none establishes a tradable signal.
Fitting is explicit so parameters can be estimated before the evaluation period.
"""
from dataclasses import dataclass

import numpy as np
from statsmodels.tsa.stattools import adfuller, coint
from statsmodels.tsa.vector_ar.vecm import coint_johansen


def _matrix(values, *, columns=None, min_rows=20, reject_constant=True):
    data = np.asarray(values, dtype=float)
    if data.ndim != 2 or len(data) < min_rows or (columns and data.shape[1] != columns):
        raise ValueError('expected a two-dimensional sample with sufficient observations')
    if not np.isfinite(data).all():
        raise ValueError('sample must contain only finite values')
    if reject_constant and np.any(np.std(data, axis=0) == 0):
        raise ValueError('constant columns are not supported')
    return data


def hurst_variance_scale(values, scales=(2, 4, 8, 16, 32)):
    """Slope/2 of log variance of lagged increments versus log lag.

    This scale-dependent heuristic assumes roughly power-law behaviour. It is
    not a hypothesis test or a general-purpose Hurst estimator.
    """
    data = np.asarray(values, dtype=float)
    if data.ndim != 1 or not np.isfinite(data).all():
        raise ValueError('expected a finite one-dimensional series')
    if len(scales) < 2 or len(set(scales)) != len(scales):
        raise ValueError('need distinct lag scales')
    if any(not isinstance(lag, (int, np.integer)) or lag <= 0 or lag >= len(data) // 2 for lag in scales):
        raise ValueError('lags must be positive integers smaller than half the sample')
    variances = [np.var(data[lag:] - data[:-lag], ddof=1) for lag in scales]
    if not np.isfinite(variances).all() or min(variances) <= 0:
        raise ValueError('lagged increments must have positive finite variance')
    return float(np.polyfit(np.log(scales), np.log(variances), 1)[0] / 2)


def adf_summary(values):
    """ADF with constant and AIC lag selection; null is a unit root."""
    data = np.asarray(values, dtype=float)
    if data.ndim != 1 or len(data) < 30 or not np.isfinite(data).all() or np.std(data) == 0:
        raise ValueError('ADF requires at least 30 finite, nonconstant observations')
    stat, pvalue, usedlag, nobs, _, _ = adfuller(data, regression='c', autolag='AIC')
    return {'statistic': float(stat), 'pvalue': float(pvalue), 'lags': int(usedlag), 'nobs': int(nobs)}


@dataclass(frozen=True)
class PairFit:
    intercept: float
    hedge_ratio: float

    def spread(self, values):
        x = _matrix(values, columns=2, min_rows=1, reject_constant=False)
        return x[:, 1] - self.intercept - self.hedge_ratio * x[:, 0]


def fit_pair(train):
    """OLS of second level on first, including intercept, on training data."""
    x = _matrix(train, columns=2)
    intercept, hedge = np.linalg.lstsq(np.column_stack((np.ones(len(x)), x[:, 0])), x[:, 1], rcond=None)[0]
    return PairFit(float(intercept), float(hedge))


def pair_cointegration(train):
    """Engle-Granger test with intercept; null is no cointegration.

    The special residual-based p-value is not the ordinary ADF p-value.
    """
    x = _matrix(train, columns=2, min_rows=30)
    stat, pvalue, _ = coint(x[:, 1], x[:, 0], trend='c', autolag='aic')
    if not np.isfinite([stat, pvalue]).all():
        raise ValueError('cointegration is undefined for this sample')
    return {'statistic': float(stat), 'pvalue': float(pvalue)}


@dataclass(frozen=True)
class PCAFit:
    centre: np.ndarray
    components: np.ndarray
    explained_ratio: np.ndarray

    def transform(self, values):
        x = _matrix(values, min_rows=1, reject_constant=False)
        if x.shape[1] != len(self.centre):
            raise ValueError('column count differs from fitted sample')
        return (x - self.centre) @ self.components.T


def fit_pca(train):
    """Unscaled centred level PCA. Signs are arbitrary; not a cointegration test."""
    x = _matrix(train)
    centre = x.mean(axis=0)
    _, singular_values, vt = np.linalg.svd(x - centre, full_matrices=False)
    variance = singular_values ** 2
    return PCAFit(centre, vt, variance / variance.sum())


def johansen_summary(train):
    """Trace statistics using the constant specification (det_order=0).

    Uses one lag of differences. Compare with tabulated 95% critical values;
    this sample-dependent diagnostic is not a guarantee of stable rank.
    """
    x = _matrix(train, min_rows=30)
    if x.shape[1] < 2 or x.shape[1] > 12:
        raise ValueError('Johansen requires 2 to 12 series')
    if np.linalg.matrix_rank(np.column_stack((np.ones(len(x)), x))) < x.shape[1] + 1:
        raise ValueError('Johansen requires linearly independent columns')
    result = coint_johansen(x, det_order=0, k_ar_diff=1)
    return {'trace': result.lr1.tolist(), 'critical_95': result.cvt[:, 1].tolist()}


def synthetic_curves(n=800, seed=42):
    """Three synthetic, same-unit series; shared stochastic trend plus AR noise."""
    if n < 60:
        raise ValueError('need at least 60 observations')
    rng = np.random.default_rng(seed)
    trend = np.cumsum(rng.normal(0, 0.30, n))
    noise = np.zeros((n, 3))
    innovations = rng.normal(0, 0.20, (n, 3))
    for t in range(1, n):
        noise[t] = 0.7 * noise[t - 1] + innovations[t]
    return trend[:, None] * np.array([1.0, 1.2, 0.8]) + noise
