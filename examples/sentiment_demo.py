"""Small synthetic evaluation of conservative entity and sentiment rules."""
from datetime import date
from pathlib import Path
from lamat_quant.sentiment import Entity, evaluate, load_fixture

root = Path(__file__).resolve().parents[1]
records = load_fixture(root / 'data/fixtures/sentiment-demo.json')
# These are illustrative validity intervals, not a historical security master.
registry = [Entity('GME', date(2021, 1, 1), date(2022, 1, 1)),
            Entity('AMC', date(2021, 1, 1), date(2022, 1, 1))]
result = evaluate(records, registry)
for index, row in enumerate(result['records'], 1):
    print(f"{index}: entities={row['entities']} sentiment={row['sentiment']} "
          f"entity_correct={row['entity_correct']} sentiment_correct={row['sentiment_correct']}")
print(f"Exact entity accuracy: {result['entity_exact_accuracy']:.2f}; "
      f"sentiment accuracy: {result['sentiment_accuracy']:.2f}")
print('Synthetic hand-authored examples; not a market benchmark or trading signal.')
