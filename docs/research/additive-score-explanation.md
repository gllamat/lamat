# Explaining a synthetic additive score

An explanation that shows only feature contributions omits the reference value from which those contributions start. The recovered fraud notebook separately returned a baseline but did not include it in the displayed contribution chart. This independent example uses invented values to show how the pieces fit; it does not reproduce the historical model or data.

For a fixed linear score `intercept + Σ(weight × feature)`, choose an explicit reference vector on the same feature scale. The baseline is the model score at that reference. Each contribution is `weight × (feature - reference)`, so baseline plus all contributions reconstructs the score, subject to floating-point rounding. The reference score is generally **not** the intercept. A different reference changes the baseline and contributions while leaving the model's score unchanged.

Run:

```sh
PYTHONPATH=packages/quant-research/src python3 examples/additive_score_explanation.py
```

This is a linear score, not a probability. A nonlinear transformation such as a logistic function does not preserve additive contributions on the probability scale. The example fits no model, uses no real records, and does not establish that a reference is representative. Correlated features and alternative baselines can change how contributions are interpreted; neither the coefficients nor this decomposition establish causation, fairness, accuracy or suitability for individual decisions. Other explanation methods use different definitions of baseline and contribution, which must be checked against their own model and output scale.
