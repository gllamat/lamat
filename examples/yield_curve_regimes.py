"""Reproducible, fully synthetic yield-curve PCA and cluster demonstration."""
import argparse
from datetime import date, timedelta
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from lamat_quant.regimes import fit_regimes


def synthetic_curves(seed=2026):
    """Synthetic percent-per-annum rates; no real market source or signal."""
    rng = np.random.default_rng(seed)
    n = 180
    # Smooth level and slope processes: structure is intentionally artificial.
    t = np.arange(n)
    level = 3.0 + 0.7 * np.sin(t / 18) + rng.normal(0, .12, n)
    slope = 0.6 * np.cos(t / 27) + rng.normal(0, .07, n)
    curvature = 0.15 * np.sin(t / 10) + rng.normal(0, .04, n)
    curves = np.column_stack([level + slope, level + .2*slope + curvature, level - .5*slope])
    return [date(2020, 1, 1) + timedelta(days=int(i)) for i in t], curves


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('artifacts/yield-curve-regimes.png'))
    args = parser.parse_args()
    dates, curves = synthetic_curves()
    result = fit_regimes(dates, curves, 120)
    print('Synthetic rates in percent per annum; maturities: 2y, 5y, 10y')
    print(f'Training: {dates[0]} to {dates[119]}; held-out: {dates[120]} to {dates[-1]}')
    print('PCA explained variance:', np.round(result.pca.explained_variance_ratio_, 4))
    print('Training cluster counts:', np.bincount(result.labels[:120], minlength=3))
    print('Held-out cluster counts:', np.bincount(result.labels[120:], minlength=3))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    for label in range(3):
        for suffix, marker, name in ((slice(0, 120), 'o', 'train'), (slice(120, None), 'x', 'held-out')):
            selected = np.flatnonzero(result.labels[suffix] == label)
            idx = selected + (0 if suffix.start == 0 else 120)
            axes[0].scatter(result.scores[idx, 0], result.scores[idx, 1], s=20, marker=marker,
                            label=f'cluster {label} / {name}', color=('tab:blue', 'tab:orange', 'tab:green')[label], alpha=.8)
    axes[0].set(xlabel='PC 1', ylabel='PC 2', title='Frozen-model assignments')
    axes[0].legend(fontsize=7)
    axes[1].plot(dates, curves[:, 0], label='2y')
    axes[1].plot(dates, curves[:, 1], label='5y')
    axes[1].plot(dates, curves[:, 2], label='10y')
    axes[1].axvline(dates[120], color='black', linestyle='--', label='held-out starts')
    axes[1].set(ylabel='Synthetic rate (% per annum)', title='Synthetic curves and split')
    axes[1].legend(fontsize=8)
    fig.suptitle('Illustrative regime analysis — synthetic data only')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=130)
    plt.close(fig)
    print('Wrote', args.output)


if __name__ == '__main__':
    main()
