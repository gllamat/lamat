# Research integration boundaries

**Review date:** 17 November 2026. This map covers the public `gllamat/lamat` repository and the named public pull requests only. It records design decisions for [issue #17](https://github.com/gllamat/lamat/issues/17); it does not make any private material public or claim that pending pull requests are integrated. Revision references below are snapshots: recheck each pull request and `main` before relying on them.

## Dependency map

```text
MAIN (merged public foundation)
  synthetic-rates.json -> JsonRatesFixture -> RatesDataset -> butterfly()
                                                   -> explicit conversion -> ordered values
  OUParameters / fit_ou / forecast                    |
        |                                            |
        +-> PR #27 OU simulator -> synthetic marks -> backtest / split evaluation

PENDING, separate research slices (no dependency on one another)
  PR #29 synthetic_curves -> training arrays -> OLS pair / PCA / ADF / EG / Johansen
  PR #28 synthetic_curves -> dated 2D array -> training scaler / PCA / k-means -> chart
  PR #31 local synthetic JSON -> as-of registry -> entity rules + sentiment -> evaluation
```

Arrows show actual calls or illustrative data flow, **not** a currently implemented adapter. PR #27 imports `OUParameters` from the merged foundation. PRs #28, #29 and #31 define separate inputs and examples; no common ingestion, chart, calendar, split or provenance interface currently connects them. All pending examples use synthetic or hand-authored data and make no market-performance claim.

| Public component | State at review | Input/output and present limit | Reuse decision |
| --- | --- | --- | --- |
| `rates.py`: `RatesProvider`, `JsonRatesFixture`, `RatesDataset` | Merged | Dated 2y/5y/10y observations; fixture accepts percent per annum with recorded source, licence, revision and missing-data policies. Dates must increase; no calendar-gap, as-of or actual revision handling. | Keep as the narrow rates input boundary. Do not pretend its three fixture rows are sufficient for a model. A real provider needs licence, availability/as-of and vintage semantics before use. |
| `mean_reversion.py`: `butterfly`, `fit_ou`, `OUParameters.forecast` | Merged | Butterfly preserves input rate units; OU takes an equally spaced scalar sequence with `dt` and returns parameters or conditional mean and standard deviation. | Reuse explicit numerical primitives. Record rate vs price units and time units; a fit is not a stationarity test or tradability evidence. |
| `backtest.py`: `simulate_ou`, `ThresholdRule`, `run_backtest`, `evaluate_chronologically` | [PR #27](https://github.com/gllamat/lamat/pull/27), `b3550c2` | Synthetic linear marks; signals use the current observation after marking prior positions. Fixed cost per unit of turnover; split segments start and finish flat. No timestamps or unit conversion. | Keep the P&L engine isolated from data providers and diagnostics. Do not feed rate changes as money P&L without a documented instrument, multiplier, sign, cashflow and mark convention. Parameter selection and point-in-time input remain the caller's responsibility. |
| `discovery.py`: pair, PCA, ADF, Engle–Granger and Johansen | [PR #29](https://github.com/gllamat/lamat/pull/29), `59952d4` | NumPy arrays; pair/PCA fit on supplied samples, then transform held-out rows. Unscaled centred level PCA. Statistical outputs are exploratory. | Keep model fitting separate from data selection and strategy rules. Document null hypotheses, in-sample choices and holdout provenance. Do not infer a common PCA API with the regime model merely because both say PCA. |
| `regimes.py`: `fit_regimes` | [PR #28](https://github.com/gllamat/lamat/pull/28), `552e5a2` | Strictly ordered date objects and finite 2D curves; scaler, PCA and k-means fit on training only, then transform full data. Training standardization differs from PR #29's unscaled PCA. | Treat the frozen transform/model and chronological cutoff as a unit. Retrospective charts must not be presented as live signals. The chart currently belongs to the example, not a shared visualization API. |
| `sentiment.py`: fixture loading, `resolve_entities`, `score_sentiment`, `evaluate` | [PR #31](https://github.com/gllamat/lamat/pull/31), `12ca31a` | Synthetic labelled UTF-8 JSON; as-of cashtags use a mock valid-from/inactive-until registry; small token lexicon evaluates sentence labels. | Keep text ingestion, entity resolution, scoring and evaluation independent. Registry dates are invented and the six examples are not a benchmark. Real ingestion needs permitted access, timestamp/availability semantics, revision and retention policies and an independently labelled corpus. |

## Minimum handoff contracts before connecting modules

1. **Data and provenance:** carry source, licence, dataset version, units, tenor/instrument identifiers, observation and availability timestamps, time zone, revision/vintage and missing-data/calendar policy. The existing `Provenance` fields are useful but do not establish a point-in-time history. Never silently discard metadata at an adapter boundary.
2. **Alignment and validation:** define how dates, tenor order and missing or revised observations are handled, fail on duplicates or non-finite data, and document conversions. A finite ordered array is not evidence that data were available at the modeled time. Test boundary failures independently rather than trusting formatting alone.
3. **Training and evaluation:** define a cutoff, select and fit parameters only on admissible training observations, freeze them for the held-out period, and record fit/sample versions. PR #27's split helper does not prohibit a caller from selecting a rule on future observations. PR #28's labels before its cutoff are in-sample and its full chart is retrospective.
4. **Units and execution:** state price versus yield, percent versus basis points, calendar/time units, instrument sign and multiplier, trade timing, transaction-cost unit and position constraints before any P&L calculation. The current butterfly is in the same rate units as its inputs; PR #27 uses linear marks and fixed per-unit costs, not a bond-pricing engine.
5. **Visualization and output:** return model results and provenance separately from chart rendering; label synthetic data, analysis date, training/test split, assumptions and uncertainty. The existing regime PNG is generated by its example. Defer a shared plotting library until at least two reviewed uses establish a stable contract.

## Dependency and integration checks

- The merged core uses the Python standard library and declares Python 3.9+. PR #27 and PR #31 also use the standard library. PR #29 adds a separate bounded NumPy/SciPy/statsmodels requirements file and statistics CI. PR #28 adds a `regimes` optional extra for bounded NumPy/scikit-learn/matplotlib and a separate CI workflow. Neither scientific dependency set is a complete lockfile; exact transitive versions, BLAS and numerical results may vary.
- PR #29 does not modify `pyproject.toml`, while PR #28 introduces an optional-dependencies table. Preserve both workflows and test suites when integrating. Use isolated environments for each documented dependency set, and test a combined environment only after the branches are actually integrated; do not assume compatibility solely because independent PR checks passed.
- Before marking integrated work complete, verify current PR heads and CI, apply or merge each reviewed branch without losing the others' additions, run the standard-library suite and each optional suite, run all examples and regenerate the regime chart, then test unit conversions, cutoff isolation and metadata preservation across any new adapter. Re-run GitHub checks against the resulting integrated commit. The separate PR checks are evidence for each branch, not proof of combined behavior.
- Later QTrader/Deep Q work and a common security master are outside this map's implementation; revisit their boundaries when concrete public interfaces exist. Do not assume a strategy environment can use the linear-mark backtester unchanged.

## Public and private publication decisions

Follow [publication-boundaries.md](publication-boundaries.md): public historical work may be **linked** with its dates and contributors, while copying its text, data, images or code requires checking the applicable rights. Newly created examples may be published after review with synthetic or properly licensed inputs and clear provenance. Private-source code, data, names, descriptions, screenshots, client details and derived disclosures stay out of public branches and issues unless the owner approves each specific disclosure and any third-party consent is obtained.

This map is based only on public repository and PR content; no private architecture or implementation is reproduced here. Before pushing, inspect the exact diff, fixtures, generated outputs and logs for secrets, personal or third-party content and accidental private material. Do not copy historical credentials even if visible in older source history. Obtain a specific publication decision for a proposed private-derived artifact rather than treating an implementation analogy as permission.
