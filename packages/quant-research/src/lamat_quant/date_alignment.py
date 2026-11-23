"""Exact session-date alignment for two independent price series."""

from dataclasses import dataclass
from datetime import date
import math
from typing import Tuple


@dataclass(frozen=True)
class DateAlignment:
    matched: Tuple[Tuple[date, float, float], ...]
    left_only: Tuple[date, ...]
    right_only: Tuple[date, ...]


def _index_observations(observations):
    indexed = {}
    for day, raw_value in observations:
        # A datetime is not a session label: callers must choose their convention.
        if type(day) is not date:
            raise ValueError("session labels must be dates, not timestamps")
        if day in indexed:
            raise ValueError("duplicate session date")
        try:
            value = float(raw_value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("prices must be finite and positive") from exc
        if not math.isfinite(value) or value <= 0:
            raise ValueError("prices must be finite and positive")
        indexed[day] = value
    return indexed


def align_by_date(left, right):
    """Join (session date, price) pairs exactly, reporting dates omitted by the join.

    Order of input rows does not affect the result. No interpolation or forward
    filling is performed; duplicate dates are rejected rather than chosen silently.
    """
    a, b = _index_observations(left), _index_observations(right)
    a_dates, b_dates = set(a), set(b)
    return DateAlignment(
        tuple((day, a[day], b[day]) for day in sorted(a_dates & b_dates)),
        tuple(sorted(a_dates - b_dates)),
        tuple(sorted(b_dates - a_dates)),
    )
