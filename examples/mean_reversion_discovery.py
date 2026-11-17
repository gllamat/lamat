"""Compare exploratory persistence, PCA and cointegration using synthetic data."""
from lamat_quant.discovery import (adf_summary, fit_pair, fit_pca, hurst_variance_scale,
                                   johansen_summary, pair_cointegration, synthetic_curves)


def main():
    data = synthetic_curves()
    train, test = data[:600], data[600:]
    pair = fit_pair(train[:, :2])
    pca = fit_pca(train)
    johansen = johansen_summary(train)
    print('Synthetic curves: seed 42; 600 training and 200 held-out observations')
    print('Heuristic H, first level / training spread:',
          round(hurst_variance_scale(train[:, 0]), 3), '/', round(hurst_variance_scale(pair.spread(train[:, :2])), 3))
    print('ADF first level p / training spread p:',
          round(adf_summary(train[:, 0])['pvalue'], 4), '/', round(adf_summary(pair.spread(train[:, :2]))['pvalue'], 4))
    print('Engle-Granger pair p (training):', round(pair_cointegration(train[:, :2])['pvalue'], 4))
    print('Pair intercept / hedge ratio (training):', round(pair.intercept, 3), '/', round(pair.hedge_ratio, 3))
    print('Held-out spread ADF p (descriptive):', round(adf_summary(pair.spread(test[:, :2]))['pvalue'], 4))
    print('PCA training variance shares:', [round(float(x), 3) for x in pca.explained_ratio])
    print('Johansen trace / 95% critical values:', [round(x, 2) for x in johansen['trace']], '/', [round(x, 2) for x in johansen['critical_95']])
    print('No trading P&L, market data or investment claim.')


if __name__ == '__main__':
    main()
