"""Explain an invented score for an invented observation."""
from lamat_quant.additive_explanation import explain_linear_score


def main():
    explanation = explain_linear_score(
        intercept=0.1,
        weights={"feature_a": 0.4, "feature_b": -0.2},
        features={"feature_a": 2.0, "feature_b": 1.0},
        reference={"feature_a": 1.0, "feature_b": 1.0},
    )
    print(f"Reference score: {explanation.baseline:.2f}")
    for name, value in explanation.contributions:
        print(f"{name}: {value:+.2f}")
    print(f"Linear score: {explanation.score:.2f}")


if __name__ == "__main__":
    main()
