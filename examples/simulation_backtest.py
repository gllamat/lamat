"""An illustrative deterministic simulation, not a market-data backtest."""
from lamat_quant.backtest import ThresholdRule, evaluate_chronologically, simulate_ou
from lamat_quant.mean_reversion import OUParameters

marks = simulate_ou(OUParameters(mean=0.0, theta=1.0, sigma=0.4), 0.0, 1 / 252, 600, seed=2026)
# This rule is fixed in advance for illustration, not fitted on the test period.
rule = ThresholdRule(centre=0.0, entry=0.25, exit=0.05, size=1.0)
train, test = evaluate_chronologically(marks, split_index=400, rule=rule, cost_per_unit=0.01)
for name, result in [('First segment', train), ('Later segment', test)]:
    print(f'{name}: observations={len(result.rows)}, gross={result.gross_pnl:.4f}, '
          f'costs={result.costs:.4f}, net={result.net_pnl:.4f}')
print('Synthetic linear marks and fixed illustrative costs; not investment performance.')
