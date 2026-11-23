"""Small binary-classification evaluation helpers for teaching examples."""

from dataclasses import dataclass
from typing import Optional, Sequence


@dataclass(frozen=True)
class BinaryMetrics:
    true_positive: int
    false_positive: int
    true_negative: int
    false_negative: int
    precision: Optional[float]
    recall: Optional[float]
    false_positive_rate: Optional[float]
    accuracy: float


def binary_metrics(actual: Sequence[int], predicted: Sequence[int]) -> BinaryMetrics:
    """Evaluate binary labels; undefined ratios are None, never zero by assumption."""
    if not actual or len(actual) != len(predicted):
        raise ValueError("actual and predicted must have equal, nonzero length")
    if any(x not in (0, 1) for x in (*actual, *predicted)):
        raise ValueError("labels must be 0 or 1")
    tp = sum(a == 1 and p == 1 for a, p in zip(actual, predicted))
    fp = sum(a == 0 and p == 1 for a, p in zip(actual, predicted))
    tn = sum(a == 0 and p == 0 for a, p in zip(actual, predicted))
    fn = sum(a == 1 and p == 0 for a, p in zip(actual, predicted))
    return BinaryMetrics(tp, fp, tn, fn,
                         tp / (tp + fp) if tp + fp else None,
                         tp / (tp + fn) if tp + fn else None,
                         fp / (fp + tn) if fp + tn else None,
                         (tp + tn) / len(actual))
