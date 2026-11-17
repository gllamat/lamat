# Deep Q comparison on synthetic prices

The historical [DeepQ Trader notebook](https://colab.research.google.com/gist/gjlr2000/62561e11e1044aa5d06e7abe2b757522/deepq_trader_public.ipynb) used a Keras neural approximation in an older software environment. This independent teaching experiment revisits the idea; it does not run, reproduce or validate the historical notebook or its results. It uses maintained Python 3.9+ and only the standard library.

## Historical assessment

The [inspected public revision](https://gist.github.com/gjlr2000/62561e11e1044aa5d06e7abe2b757522/4f5b2034554fbd6575da700f8578a7e06e070f53) has two 22-unit hard-sigmoid layers, 11 linear outputs, Adam and a squared-error loss. Its actions change holdings rather than select target holdings; it models spread and quadratic impact, and penalizes squared P&L in its reward. Its training method bootstraps from the same network and declares memory but the inspected simple training loop does not use replay. Its out-of-sample method calls the epsilon-greedy action method, so exploration may remain active. The present experiment instead uses three target positions, a fixed turnover cost, unpenalized linear P&L, a smaller tanh network, a periodically copied target network, no replay and frozen greedy evaluation. These differences prevent a direct numerical comparison with the old notebook. The source was inspected without executing its legacy dependencies or saved outputs.

## Design

Both learners use the [QTrader synthetic environment](qtrader-teaching.md): the same bounded mean-reverting price generator, target holdings, timing, costs, terminal liquidation, and linear P&L reward. The neural learner uses current normalized price and holding as inputs, eight tanh hidden units and three Q outputs. Online one-step Q-learning uses epsilon-greedy exploration and a target network copied every 100 updates, with clipped prediction error; it has no replay buffer. Terminal targets do not bootstrap. The network approximates an infinite-horizon state value without a remaining-time feature. It is deliberately small and is not presented as a faithful implementation of the old Keras model.

Run the comparison from the repository root:

```sh
PYTHONPATH=packages/quant-research/src python3 examples/deep_q_comparison.py
PYTHONPATH=packages/quant-research/src python3 -m unittest discover -s packages/quant-research/tests
```

Each learner trains on 200 generated episodes of 200 steps, using seed 7. Their training streams differ: the baseline shares one random stream for prices and actions, whereas the neural learner separates price, exploration and initialization streams. The frozen policies are evaluated on the same 50 new paths generated with seed 9001; flat and a threshold that knows the synthetic centre are also reported. The parameters and seeds are fixed in advance. Mean gross, turnover costs and net P&L are arbitrary linear units, not returns. This one comparison does not establish statistical significance, tune models, or show superiority. Neither the synthetic generator nor the threshold's privileged knowledge represents a market; no capital, financing, realistic execution, slippage, risk management or real data are modelled.
