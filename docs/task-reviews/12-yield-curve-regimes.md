# Task 12: yield-curve regime analysis — review record

**Board task:** [Refresh yield-curve regime analysis](https://github.com/gllamat/lamat/issues/12). **Status:** ready for review.

## Deliverables

- [Methodology and reproducible commands](../research/yield-curve-regimes.md).
- [Generated chart](../research/assets/yield-curve-regimes.png) and [research model](../../packages/quant-research/src/lamat_quant/regimes.py), [synthetic example and chart](../../examples/yield_curve_regimes.py), and [tests](../../packages/quant-research/regime_tests/test_regimes.py).
- Separate optional `regimes` dependencies and CI workflow; the original standard-library example remains independent.

The model fits standardization, PCA and k-means on training rows only, then applies the frozen objects to held-out rows. The synthetic chart shows PCA-space assignments and an explicit chronological split. It is a retrospective visual, not a trading recommendation, market observation or claim that stable economic regimes exist.

## Review and verification

Run the commands in the methodology. Tests verify that altering all held-out values cannot change fitted scaling, components, centroids or training labels; check the held-out prediction path, reproducibility, date alignment and rejection of invalid data. The example produces a PNG and reports its date split and sample counts. CI runs the optional example and tests on Python 3.9 and 3.13. Inspect the split, assumptions and chart, as well as the separate GitHub workflow results.

Remaining limitations include unsupervised model-selection risk, lack of a dependency lockfile, no data revision or availability model, no business-day handling, no stability test against real rates and no live signal or performance evaluation. The exact number of clusters and components is illustrative. A genuine market-data and walk-forward study remains future work.
