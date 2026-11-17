# Task 6: mean-reversion model validation — review record

**Status:** Prepared for review; changes have not yet been merged.  
**Reviewed:** 17 November 2026.  
**Board task:** [Validate the existing OU research module](https://github.com/gllamat/lamat/issues/6).

## What was checked

The Ornstein–Uhlenbeck transition gives mean `mu + (x - mu) exp(-theta t)` and variance `sigma²(1 - exp(-2 theta t)) / (2 theta)`. The fit interprets a discrete autoregression `y = a + phi x` as `theta = -log(phi)/dt` and `mu = a/(1-phi)` when `0 < phi < 1`.

[Independent numerical checks](../../packages/quant-research/tests/test_ou_validation.py) cover a half-life with an analytically known conditional mean and variance, an exact autoregressive sequence with known parameters, time-unit conversion, zero volatility, a very short time horizon and invalid inputs. The existing seeded synthetic recovery test remains in place. These checks test examples of the formulas, not every possible input.

## Reproduce

```sh
PYTHONPATH=packages/quant-research/src python3 -m unittest discover -s packages/quant-research/tests
```

## Limits to review

The estimator assumes equally spaced observations and a constant-parameter OU model. A valid fit is not a stationarity test or evidence of a profitable strategy. The review does not establish confidence intervals, robustness to irregular sampling or outliers, or performance on real data. Sigma is expressed per square root of the chosen time unit and theta per unit; changing `dt` changes both conventions. The existing synthetic recovery test uses a fixed seed and a tolerance, not a proof of estimator accuracy.

**Human review:** inspect the tests and their expected values, run the command, and review the linked pull request and automated checks before approving integration. The board card should move to Done after the change is merged.
