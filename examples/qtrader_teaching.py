"""Seeded tabular Q-learning on bounded synthetic prices; not a trading strategy."""
from lamat_quant.qtrader import Config, evaluate, train

cfg = Config()
table = train(cfg, episodes=200, steps=200, seed=7)
print(f'Training: 200 synthetic episodes, 200 steps, seed 7; visited states: {len(table)}')
print('Held-out: 50 independent synthetic episodes, 200 steps, seed 9001')
for policy in ('learned', 'flat', 'threshold'):
    results = evaluate(cfg, table, episodes=50, steps=200, seed=9001, policy=policy)
    means = [sum(x[i] for x in results) / len(results) for i in range(3)]
    print(f'{policy:9s} mean gross={means[0]:.3f} costs={means[1]:.3f} net={means[2]:.3f}')
print('Illustrative linear P&L only; no real prices, capital, Sharpe, or trading claim.')
