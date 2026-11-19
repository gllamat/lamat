"""A deterministic synthetic rolling-origin baseline; not market data."""
from datetime import date, timedelta
from math import sin

from lamat_quant.forecast_evaluation import evaluate_rolling_mean


def main():
    dates = [date(2020, 1, 1) + timedelta(days=i) for i in range(80)]
    rates = [3 + 0.01 * i + 0.2 * sin(i / 5) for i in range(80)]
    result = evaluate_rolling_mean(rates, train_end=50, lookback=5, horizon=3)
    print('Synthetic illustration; rates and dates are invented.')
    print(f'Training ends {dates[49]}; fixed scaling range {result.train_min:.3f}–{result.train_max:.3f}.')
    print('Forecasts are rolling-origin; horizon is measured in observations.')
    for forecast in result.forecasts[:5]:
        print(f'{dates[forecast.origin]} -> {dates[forecast.target]}: '
              f'predicted {forecast.prediction:.3f}, actual {forecast.actual:.3f}')
    mae = sum(abs(f.prediction - f.actual) for f in result.forecasts) / len(result.forecasts)
    print(f'Illustrative held-out MAE: {mae:.3f}; no real-world performance claim.')


if __name__ == '__main__':
    main()
