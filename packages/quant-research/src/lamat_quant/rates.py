"""Validated, replaceable input for dated 2y/5y/10y rate observations."""
from dataclasses import dataclass
from datetime import date
import json
import math
from pathlib import Path
from typing import Protocol, Tuple


@dataclass(frozen=True)
class Provenance:
    source: str
    licence: str
    units: str
    revision_policy: str
    missing_data_policy: str


@dataclass(frozen=True)
class RateObservation:
    observation_date: date
    two_year: float
    five_year: float
    ten_year: float


@dataclass(frozen=True)
class RatesDataset:
    provenance: Provenance
    observations: Tuple[RateObservation, ...]


class RatesProvider(Protocol):
    def load(self) -> RatesDataset:
        """Return observations with their source and conventions."""
        ...


class JsonRatesFixture:
    """Read a small local fixture; no network or live market data involved."""

    def __init__(self, path):
        self.path = Path(path)

    def load(self) -> RatesDataset:
        with self.path.open(encoding="utf-8") as stream:
            raw = json.load(stream)
        metadata = raw.get("provenance")
        if not isinstance(metadata, dict):
            raise ValueError("provenance must be an object")
        names = ("source", "licence", "units", "revision_policy", "missing_data_policy")
        if any(not isinstance(metadata.get(name), str) or not metadata[name].strip() for name in names):
            raise ValueError("all provenance fields must be nonempty strings")
        if metadata["units"] != "percent per annum":
            raise ValueError("fixture rates must use percent per annum")
        if metadata["missing_data_policy"] != "reject":
            raise ValueError("fixture missing-data policy must be reject")
        rows = raw.get("observations")
        if not isinstance(rows, list) or not rows:
            raise ValueError("at least one observation is required")
        observations = []
        for row in rows:
            try:
                day = date.fromisoformat(row["date"])
                values = (row["2y"], row["5y"], row["10y"])
                if any(isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) for value in values):
                    raise ValueError("rates must be finite numbers")
            except (TypeError, KeyError, ValueError) as exc:
                raise ValueError("invalid rate observation") from exc
            if observations and day <= observations[-1].observation_date:
                raise ValueError("observation dates must be strictly increasing")
            observations.append(RateObservation(day, *values))
        return RatesDataset(Provenance(*(metadata[name] for name in names)), tuple(observations))
