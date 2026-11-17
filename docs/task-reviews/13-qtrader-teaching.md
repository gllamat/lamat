# Task 13: QTrader teaching experiment — review record

**Status:** Prepared for review. [Board task](https://github.com/gllamat/lamat/issues/13).

## Deliverable

Review the [model description and limitations](../research/qtrader-teaching.md), [environment, Q learner and evaluation](../../packages/quant-research/src/lamat_quant/qtrader.py), [seeded example](../../examples/qtrader_teaching.py) and [tests](../../packages/quant-research/tests/test_qtrader.py). The historical notebook is linked and distinguished from the new implementation. The example compares a frozen learned policy with a flat baseline and a fixed threshold on the same separately seeded synthetic evaluation paths.

## Verification

```sh
PYTHONPATH=packages/quant-research/src python3 examples/qtrader_teaching.py
PYTHONPATH=packages/quant-research/src python3 -m unittest discover -s packages/quant-research/tests
```

All 13 tests passed locally. Tests cover a hand-calculated trade and position flip, both opening and terminal costs, flat tie-breaking, no future-price input to action selection, deterministic training/evaluation, frozen policy, bounded synthetic marks and invalid parameters. Review the execution convention and reward before integration. Evaluation uses a known synthetic process with a threshold benchmark that knows its centre; it is not a real-world or independent-regime study.

## Limitations

The environment has simplified price dynamics and holding constraints; reward is linear P&L less fixed costs, not the historical risk-adjusted objective. Evaluation does not model data leakage in external model selection, transaction market impact, financing, capital or risk constraints. It does not establish profitable or robust performance. The original notebook was inspected for its narrative but not run.
