# Task 14 review: Deep Q teaching comparison

## Decision and scope

Add a deterministic, synthetic neural Q-function teaching experiment alongside the merged tabular baseline. The neural model is an independent standard-library implementation, not a reproduction of the historical Keras notebook. The example compares frozen learners and two references on identical held-out synthetic paths. The research note explains model timing, reward, differences in training streams and limits of interpretation.

## Reviewer checks

- Inspect `packages/quant-research/src/lamat_quant/deep_q.py`, `examples/deep_q_comparison.py`, and `docs/research/deep-q-comparison.md`.
- Run the example and the research package test suite using the commands in the research note.
- Confirm this synthetic demonstration and the historical link are suitable to publish. No actual trading or performance claim is made.

The result is a single pre-specified comparison, not a statistical study or an operational strategy. The public notebook source was inspected and material differences in architecture, actions, reward, costs and evaluation are recorded in the research note. It was not executed; its legacy dependencies and performance have not been validated.
