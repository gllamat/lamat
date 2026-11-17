"""Offline, illustrative financial text evaluation. No live data ingestion."""
from dataclasses import dataclass
from datetime import date
import json
from pathlib import Path
import re


@dataclass(frozen=True)
class Entity:
    symbol: str
    valid_from: date
    valid_until: date  # exclusive


def load_fixture(path):
    """Read local, manually authored records; reject missing or malformed fields."""
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if data.get('provenance') != 'synthetic hand-authored examples':
        raise ValueError('fixture provenance must identify synthetic examples')
    records = data['records']
    if not isinstance(records, list) or not records:
        raise ValueError('records must be a nonempty list')
    for row in records:
        if not isinstance(row.get('text'), str) or not row['text'].strip():
            raise ValueError('text must be nonempty')
        date.fromisoformat(row['date'])
        if row.get('sentiment') not in ('positive', 'negative', 'neutral'):
            raise ValueError('invalid sentiment label')
        if not isinstance(row.get('entities'), list):
            raise ValueError('entities must be a list')
    return records


def resolve_entities(text, as_of, registry):
    """Resolve explicit uppercase cashtags against an as-of registry.

    This deliberately conservative teaching rule cannot resolve company names,
    bare tickers or non-equity instruments. A cashtag is not proof of intent.
    """
    if not isinstance(as_of, date):
        raise ValueError('as_of must be a date')
    active = {e.symbol for e in registry if e.valid_from <= as_of < e.valid_until}
    return sorted(set(re.findall(r'(?<![A-Za-z0-9_$])\$([A-Z]{1,5})(?![A-Za-z0-9_])', text)) & active)


# Small hand-written teaching lexicon, not a trained model or validated dictionary.
_POSITIVE = {'beats', 'beat', 'profit', 'growth', 'gain', 'rally'}
_NEGATIVE = {'misses', 'miss', 'loss', 'decline', 'fall', 'fraud'}


def score_sentiment(text):
    """Return a simple token count label; context, negation and sarcasm are ignored."""
    tokens = re.findall(r"[a-z]+", text.lower())
    score = sum(t in _POSITIVE for t in tokens) - sum(t in _NEGATIVE for t in tokens)
    return 'positive' if score > 0 else 'negative' if score < 0 else 'neutral'


def evaluate(records, registry):
    """Per-record outputs and exact-match accuracy; labels are illustrative."""
    if not records:
        raise ValueError('evaluation requires at least one record')
    out = []
    for row in records:
        predicted_entities = resolve_entities(row['text'], date.fromisoformat(row['date']), registry)
        predicted_sentiment = score_sentiment(row['text'])
        out.append({'entities': predicted_entities, 'sentiment': predicted_sentiment,
                    'entity_correct': predicted_entities == sorted(set(row['entities'])),
                    'sentiment_correct': predicted_sentiment == row['sentiment']})
    return {'records': out,
            'entity_exact_accuracy': sum(x['entity_correct'] for x in out) / len(out),
            'sentiment_accuracy': sum(x['sentiment_correct'] for x in out) / len(out)}
