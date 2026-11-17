"""Fit an illustrative curve-regime model with strictly training-only transforms.

This is exploratory statistical clustering, not a strategy or market forecast.
"""
from dataclasses import dataclass
from datetime import date

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


@dataclass(frozen=True)
class RegimeResult:
    """Fitted model and date-aligned in-sample and held-out assignments."""
    dates: tuple
    train_size: int
    scaler: StandardScaler
    pca: PCA
    clusters: KMeans
    scores: np.ndarray
    labels: np.ndarray


def fit_regimes(dates, curves, train_size, *, components=2, clusters=3, seed=2026):
    """Standardize, fit PCA and fit k-means only on the first train_size curves.

    Dates must be strictly ascending date objects, and curves a finite numeric
    array in consistent units and maturity order. No missing values are imputed.
    The returned suffix assignments use the frozen in-sample model.
    """
    dates = tuple(dates)
    values = np.asarray(curves, dtype=float)
    if values.ndim != 2 or values.shape[0] != len(dates) or values.shape[1] < 2:
        raise ValueError('curves must be a date-aligned 2-D array with at least two maturities')
    if any(not isinstance(d, date) for d in dates) or any(a >= b for a, b in zip(dates, dates[1:])):
        raise ValueError('dates must be strictly increasing date objects')
    if not np.isfinite(values).all():
        raise ValueError('curves must be finite; missing values are not imputed')
    if not isinstance(train_size, int) or isinstance(train_size, bool) or not 2 <= train_size < len(dates):
        raise ValueError('train_size must leave at least two training rows and one test row')
    if not isinstance(components, int) or not 1 <= components <= min(train_size - 1, values.shape[1]):
        raise ValueError('invalid PCA component count')
    if not isinstance(clusters, int) or not 2 <= clusters <= train_size:
        raise ValueError('invalid cluster count')
    train = values[:train_size]
    if np.any(np.std(train, axis=0) == 0):
        raise ValueError('each training maturity must have nonzero variance')
    scaler = StandardScaler().fit(train)
    scaled_train = scaler.transform(train)
    pca = PCA(n_components=components, svd_solver='full').fit(scaled_train)
    train_scores = pca.transform(scaled_train)
    if np.unique(train_scores, axis=0).shape[0] < clusters:
        raise ValueError('fewer distinct training points than clusters')
    model = KMeans(n_clusters=clusters, random_state=seed, n_init=10).fit(train_scores)
    scores = pca.transform(scaler.transform(values))
    return RegimeResult(dates, train_size, scaler, pca, model, scores, model.predict(scores))
