# Lamat

Research, writing and reusable tools at the intersection of quantitative finance, data science and intelligence amplification.

This repository is a work in progress. The first research slice modernizes the [original mean-reversion notebooks](https://github.com/gllamat/MeanReversion) with a small reusable Python library and an offline synthetic example. The website is a local preview, not a replacement for the existing site.

## Explore the research example

Requires Python 3.9 or later; the first slice uses only the standard library.

```sh
PYTHONPATH=packages/quant-research/src python3 examples/mean_reversion.py
PYTHONPATH=packages/quant-research/src python3 -m unittest discover -s packages/quant-research/tests
```

See [the methodology](docs/mean-reversion.md), [the source inventory](docs/source-inventory.md), and [the historical archive](apps/web/archive.html). The archive can be regenerated with `python3 scripts/build_archive.py`. The example does not use current market data and makes no performance claim.

## Local website preview

Open `apps/web/index.html` in a browser. The visual direction follows the existing Lamat wordmark and blue, black and white palette; original brand files and complete content migration still need verification.

## Repository layout

- `packages/quant-research/`: numerical functions and tests.
- `examples/`: small reproducible research examples.
- `apps/web/`: static local website preview.
- `docs/`: methodology, provenance and modernization notes.
