"""Compare frozen Q learners on identical held-out synthetic paths."""
from lamat_quant.qtrader import Config, evaluate, train
from lamat_quant.deep_q import evaluate_neural, train_neural

cfg = Config()
table = train(cfg, episodes=200, steps=200, seed=7)
network = train_neural(cfg, episodes=200, steps=200, seed=7)
print('Training: 200 synthetic episodes, 200 steps, seed 7 for each learner')
print('Held-out: 50 identical synthetic episodes, 200 steps, seed 9001')
policies = [('tabular', evaluate(cfg, table, seed=9001)),
            ('neural', evaluate_neural(cfg, network, seed=9001)),
            ('flat', evaluate(cfg, table, seed=9001, policy='flat')),
            ('threshold', evaluate(cfg, table, seed=9001, policy='threshold'))]
for name, results in policies:
    means = [sum(row[i] for row in results) / len(results) for i in range(3)]
    print(f'{name:9s} mean gross={means[0]:.3f} costs={means[1]:.3f} net={means[2]:.3f}')
print('Illustrative linear P&L only; no real prices or trading claim.')
