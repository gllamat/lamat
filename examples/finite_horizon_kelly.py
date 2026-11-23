"""Invented win/loss/no-hit scenarios; not a trading recommendation."""
from lamat_quant.kelly import Scenario, expected_log_growth, grid_search


def main():
    # First hit is mutually exclusive; no hit has a specified zero net payoff.
    scenarios = (
        Scenario(0.4, (1.0,)),
        Scenario(0.2, (-1.0,)),
        Scenario(0.4, (0.0,)),
    )
    fraction, growth = grid_search(scenarios, steps=30)
    print(f"Best grid fraction: {fraction[0]:.6f}; expected log growth: {growth:.6f}")
    print(f"No allocation: {expected_log_growth(scenarios, (0.0,)):.6f}")
    print("Analytical optimum for these assumptions: 1/3")


if __name__ == "__main__":
    main()
