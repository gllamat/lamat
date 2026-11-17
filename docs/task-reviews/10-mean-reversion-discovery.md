# Task 10: mean-reversion discovery — review record

**Status:** Prepared for review. **Task:** [Modernize mean-reversion discovery and cointegration](https://github.com/gllamat/lamat/issues/10).

## Deliverables

Read the [synthetic comparison](../tutorials/mean-reversion-discovery.md), run [the example](../../examples/mean_reversion_discovery.py), and inspect [the implementation](../../packages/quant-research/src/lamat_quant/discovery.py) and [tests](../../packages/quant-research/statistics-tests/test_discovery.py). The example compares Hurst-style variance scaling, ADF, a pairs regression and Engle–Granger, PCA and Johansen on the same seeded synthetic series. Fit parameters use training observations only; evaluation uses a chronological held-out slice.

## Reproduce

See the tutorial for a virtual environment and optional dependency setup. Run the discovery example and statistics tests with the indicated `PYTHONPATH`. The standard-library research tests and original example remain separate. Optional NumPy, SciPy and statsmodels dependencies are bounded but not fully locked; exact numerical results can vary. The companion CI workflow installs these dependencies for Python 3.9 and 3.13.

## Review boundaries

The simulation intentionally has a shared stochastic trend and stationary noise. Its apparent cointegration is constructed, not a market finding. The ADF null is a unit root; Engle–Granger's null is no cointegration; PCA is not a cointegration test. Held-out residual diagnostics are descriptive, and no returns, forecasts, costs or execution are presented. Hurst lag selection and Johansen specification require judgment. Review the assumptions and code before integration; none of the results establishes stationarity, a trading strategy or investment performance.
