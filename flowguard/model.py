"""A small, inspectable MAD-based anomaly detector."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from statistics import median
from typing import Iterable, Mapping
EPSILON = 1e-9
@dataclass
class FeatureStat:
    median: float
    mad: float
class MadAnomalyDetector:
    """Scores flows by their largest robust per-feature deviation."""
    def __init__(self, threshold: float = 4.0) -> None:
        self.threshold = threshold
        self.stats: dict[str, FeatureStat] = {}
    def fit(self, rows: Iterable[Mapping[str, float]], features: list[str]) -> "MadAnomalyDetector":
        samples = list(rows)
        if not samples: raise ValueError("at least one benign flow is required")
        for feature in features:
            values = [float(row[feature]) for row in samples]
            centre = median(values)
            self.stats[feature] = FeatureStat(centre, max(median([abs(value-centre) for value in values]), EPSILON))
        return self
    def score(self, row: Mapping[str, float]) -> dict[str, object]:
        if not self.stats: raise RuntimeError("fit the detector before scoring")
        contributions = {feature: abs(float(row[feature])-stat.median)/(1.4826*stat.mad) for feature, stat in self.stats.items()}
        score = max(contributions.values())
        return {"score": round(score, 4), "threshold": self.threshold, "anomalous": score >= self.threshold, "top_features": sorted(contributions.items(), key=lambda item: item[1], reverse=True)[:3]}
    def to_dict(self) -> dict[str, object]:
        return {"threshold": self.threshold, "stats": {name: asdict(stat) for name, stat in self.stats.items()}}
    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> "MadAnomalyDetector":
        detector = cls(float(payload["threshold"])); stats = payload["stats"]
        if not isinstance(stats, dict): raise ValueError("invalid model statistics")
        detector.stats = {name: FeatureStat(**values) for name, values in stats.items()}
        return detector
