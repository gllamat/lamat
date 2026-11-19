"""Invented European calls illustrate adjacent strike-interval averages."""
from lamat_quant.option_spreads import interval_survival


def main():
    # Invented expiry outcomes and probabilities; not observations or a forecast.
    states = [(80, .2), (105, .5), (140, .3)]
    strikes = [90, 100, 120, 145]
    discount = .95
    calls = [discount * sum(p * max(s - k, 0) for s, p in states) for k in strikes]
    print('Synthetic European calls; interval-averaged risk-neutral survival only.')
    for row in interval_survival(strikes, calls, discount):
        print(f'{row.lower_strike:g}–{row.upper_strike:g}: {row.average_survival:.3f}')
    print('These are not real-world probabilities or a complete distribution.')


if __name__ == '__main__':
    main()
