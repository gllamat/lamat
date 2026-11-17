# Task 15: financial sentiment and entity resolution — review record

**Status:** Prepared for human review. [Board task](https://github.com/gllamat/lamat/issues/15).

Read the [methodology and limitations](../research/financial-sentiment.md), inspect the [hand-authored labelled fixture](../../data/fixtures/sentiment-demo.json), [offline pipeline](../../packages/quant-research/src/lamat_quant/sentiment.py), [example](../../examples/sentiment_demo.py) and [tests](../../packages/quant-research/tests/test_sentiment.py). The original notebook's YOLO/HOLD ambiguity is retained as a regression case. Ingestion, point-in-time resolution, sentiment rules and evaluation are distinct functions; no provider API or third-party data is accessed.

The example shows two deliberate failures: the word-only lexicon ignores negation and explicit-cashtag-only matching misses a bare ticker. Both happen on a tiny, jointly authored synthetic fixture; its reported accuracy is not an external benchmark. The mock ticker validity intervals are invented. The example does not claim prediction or returns. No historical notebook data or text was copied.

Reproduce from the repository root:

```sh
PYTHONPATH=packages/quant-research/src python3 examples/sentiment_demo.py
PYTHONPATH=packages/quant-research/src python3 -m unittest discover -s packages/quant-research/tests
```

Local checks passed all 13 research tests. Review the registry semantics, labelled cases, demonstrated failures and limitations before integration. An independently labelled corpus and approved data access remain separate future work.
