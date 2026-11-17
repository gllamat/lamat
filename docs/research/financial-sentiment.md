# Financial sentiment: an offline evaluation starting point

The historical [RedditScrapNltk notebook](https://gist.github.com/gllamat/867075b3d482f82245f621f4ccda6aa8/c907a4a12725b8be97057b774e6d0210ac711443) notes that ticker matching can mistake **YOLO** and **HOLD** for symbols. The historical [sentiment notebook](https://gist.github.com/gllamat/ae758bc22f2cb5de621d893ba7b6769e/5f948ff798c33986940b6fa1856dcf79c627bc35) discusses finance-specific language and general-purpose sentiment failures. The new example preserves the ambiguity as a test, but does not copy Reddit content, historical datasets, models or credentials.

Run with Python 3.9 or later from the repository root:

```sh
PYTHONPATH=packages/quant-research/src python3 examples/sentiment_demo.py
PYTHONPATH=packages/quant-research/src python3 -m unittest discover -s packages/quant-research/tests
```

The local UTF-8 JSON fixture contains six manually authored synthetic sentences and illustrative human-assigned labels. The mock registry's dates are invented; they are not historical listing dates. The resolver accepts explicit uppercase cashtags only if their symbol is valid on the observation date, with an inclusive start and exclusive end. This intentionally conservative rule misses company names and bare symbols, and cannot disambiguate an explicit cashtag used in a non-security context. A real implementation requires an authoritative point-in-time security master, aliases, source timestamp and revision rules.

A tiny hand-authored finance-oriented lexicon counts selected positive and negative tokens; it is not a trained financial sentiment model. It ignores negation, context, sarcasm, target entities and language drift. The example explicitly shows the negation and bare-ticker failures: five of six exact entity labels and five of six sentiment labels match. The sample and scoring rules were designed together, so these fractions are **demonstration outputs, not estimates of real-world performance**. The sentence-level label does not establish an entity-specific stance. The fixture contains no price data and measures no trading return.

No network ingestion is included. Any future Reddit or other provider adapter needs current permission, access terms, privacy/retention controls, provenance and point-in-time availability. A meaningful evaluation needs a larger, independently labelled, permissioned, temporally separated corpus, measured annotator agreement and an appropriate entity-level model; economic or trading claims need separate evaluation with realistic costs and leakage controls.
