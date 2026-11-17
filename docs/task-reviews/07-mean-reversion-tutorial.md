# Task 7: mean-reversion tutorial — review record

**Status:** Ready for review, pending integration.  
**Reviewed:** 17 November 2026.  
**Board task:** [Modernize the 2s/5s/10s mean-reversion tutorial](https://github.com/gllamat/lamat/issues/7).

## Deliverable

Read the [updated tutorial](../tutorials/mean-reversion-2026.md). It explains the synthetic rates fixture, butterfly calculation, OU model, time and rate units, reproducible commands, a sample run and research limitations. It links the 2018 original and explicitly separates the fixture from the independently simulated OU series.

## Verification

From the repository root:

```sh
PYTHONPATH=packages/quant-research/src python3 examples/mean_reversion.py
PYTHONPATH=packages/quant-research/src python3 -m unittest discover -s packages/quant-research/tests
```

The example ran and printed the fixture provenance and a 0.1 percentage-point butterfly; all nine tests passed locally. GitHub checks should also pass before integration. Results are synthetic and do not demonstrate trading profitability.

**Human review:** check the clarity and accuracy of the tutorial, the original-versus-new distinction, assumptions, units and output. Review the changes and checks in the associated pull request before approving the merge.
