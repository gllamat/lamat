# Yield-curve regimes: a synthetic, chronological example

The original [rates clustering notebook](https://github.com/gllamat/Intelligence-Amplification) explored PCA and clustering as an example of intelligence amplification. The example here is a new, explicitly **synthetic** demonstration. It does not reproduce that notebook's market results, fetch historical data, or identify actual central-bank regimes.

## Method

We generate 180 daily three-tenor curves in percent per annum using seeded level, slope, curvature and noise processes. The first 120 observations (1 January–29 April 2020) are training; the last 60 (30 April–28 June 2020) are held out. Dates are illustrative calendar dates, not a business-day market calendar.

1. Fit a per-tenor mean and standard deviation **only on training observations**; transform both periods with those fixed parameters. Inputs must be finite and ordered, and each training tenor must vary. No imputation is performed.
2. Fit two principal components on standardized training curves. Transform the held-out period with that same PCA basis.
3. Fit three k-means centroids on the training PCA scores using a fixed random seed and ten initializations. Assign held-out curves to the nearest frozen centroid without refitting. Cluster labels have no inherent order or financial meaning.
4. Plot both periods in PCA space and the source curves over time, marking the split. The whole-period figure is **retrospective**; it is not itself evidence of a real-time signal. A held-out assignment can be made after that day's curve is available, with the model frozen at the training cutoff. No trading or prediction is evaluated.

Because training data are synthetic and deliberately structured, apparent groups are artefacts of this generator and method choices. Clusters can change with window, scaling, number of components or clusters, initialization, outliers, and market revisions. PCA directions are sign-indeterminate; label numbers can permute across fits. An unsupervised cluster is not proof of a stable economic regime. The example makes no claims of returns or model accuracy. Real data would need licensing, provenance, units, missing-day policy, point-in-time availability, revisions and a genuine walk-forward evaluation before any real-time use.

## Reproduce

Use Python 3.9+ and an isolated environment:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install './packages/quant-research[regimes]'
python -m unittest discover -s packages/quant-research/regime_tests
python examples/yield_curve_regimes.py --output artifacts/yield-curve-regimes.png
```

The plot is generated locally and the printed split, explained-variance ratios and cluster counts are reproducible for a fixed numerical environment. The optional package group is version-bounded, not a full lockfile: exact charts and floating-point results can vary by library version, platform and BLAS implementation. The first two principal components are an illustrative choice rather than an optimized number. See [task review](../task-reviews/12-yield-curve-regimes.md) for checks and remaining limitations.
