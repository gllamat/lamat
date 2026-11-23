"""Explain a fixed linear score relative to an explicit reference."""

from dataclasses import dataclass
import math
from typing import Mapping, Tuple


@dataclass(frozen=True)
class LinearExplanation:
    baseline: float
    contributions: Tuple[Tuple[str, float], ...]
    score: float


def explain_linear_score(intercept: float, weights: Mapping[str, float],
                         features: Mapping[str, float],
                         reference: Mapping[str, float]) -> LinearExplanation:
    """Decompose a linear score; feature values and reference use the same scale.

    The baseline is intercept + sum(weight * reference), not just the intercept.
    Contributions are weight * (feature - reference). No model is fitted.
    """
    keys = set(weights)
    if not keys or keys != set(features) or keys != set(reference):
        raise ValueError("weights, features and reference need the same nonempty keys")
    if not math.isfinite(intercept) or any(
        not math.isfinite(value)
        for mapping in (weights, features, reference)
        for value in mapping.values()
    ):
        raise ValueError("inputs must be finite")
    names = sorted(keys)
    try:
        baseline = math.fsum([intercept] + [weights[k] * reference[k] for k in names])
        contributions = tuple((k, weights[k] * (features[k] - reference[k])) for k in names)
        score = math.fsum([baseline] + [value for _, value in contributions])
    except (OverflowError, ValueError) as exc:
        raise ValueError("computed values must be finite") from exc
    if not math.isfinite(score) or not math.isfinite(baseline) or any(
        not math.isfinite(value) for _, value in contributions
    ):
        raise ValueError("computed values must be finite")
    return LinearExplanation(baseline, contributions, score)
