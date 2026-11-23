# Aligning two price series by session date

A recovered historical notebook loads two CSV files and assigns one close-price column to the other table by pandas index before plotting. With default CSV row indices, this pairs rows by position. If either file has missing or differently ordered sessions, observations from different dates can be paired. The historical CSV contents and output were not inspected, so this is a possible failure mode, not a finding that its plot was wrong.

The independent example uses invented prices and joins on explicit session-date labels, returning matched rows and both sets of unmatched dates. It does not silently fill gaps, and it rejects duplicate dates so their meaning must be resolved first.

```sh
PYTHONPATH=packages/quant-research/src python3 examples/date_alignment.py
```

A shared calendar date alone does not establish simultaneous observation or point-in-time availability. Different exchange calendars, time zones, close times, adjusted-price conventions, corporate actions and missing-data mechanisms require separate review. Excluding unmatched sessions changes the sample; inspect the reported dates and choose a policy before calculating correlations or fitting models. This is an alignment example, not evidence of a market relationship, forecast or trading performance.
