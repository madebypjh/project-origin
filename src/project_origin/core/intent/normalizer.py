"""Normalize open-ended intent signals without imposing domain categories."""

import re
from typing import Iterable

from project_origin.core.intent.models import IntentSignal


class IntentNormalizer:
    @classmethod
    def normalize(
        cls,
        signals: Iterable[IntentSignal],
    ) -> tuple[IntentSignal, ...]:
        aggregated: dict[tuple[str, str], dict] = {}

        for signal in signals:
            kind = cls._canonical_name(signal.kind)
            concept = cls._canonical_name(signal.concept)
            key = (kind, concept)
            entry = aggregated.setdefault(
                key,
                {
                    "weight": 0.0,
                    "confidence": 0.0,
                    "evidence": [],
                    "metadata": {},
                },
            )
            entry["weight"] += signal.weight
            entry["confidence"] = max(
                entry["confidence"],
                signal.confidence,
            )
            entry["evidence"].extend(signal.evidence)
            entry["metadata"].update(signal.metadata)

        if not aggregated:
            return ()

        total_weight = sum(entry["weight"] for entry in aggregated.values())
        if total_weight <= 0:
            raise ValueError("Intent signal weights must have a positive sum")

        normalized = []
        for (kind, concept), entry in aggregated.items():
            evidence = tuple(dict.fromkeys(entry["evidence"]))
            normalized.append(
                IntentSignal(
                    kind=kind,
                    concept=concept,
                    weight=round(entry["weight"] / total_weight, 4),
                    evidence=evidence,
                    confidence=entry["confidence"],
                    metadata=entry["metadata"],
                )
            )

        return tuple(
            sorted(
                normalized,
                key=lambda signal: (-signal.weight, signal.kind, signal.concept),
            )
        )

    @staticmethod
    def _canonical_name(value: str) -> str:
        normalized = value.strip().casefold()
        normalized = re.sub(r"[\s-]+", "_", normalized)
        normalized = re.sub(r"[^\w]+", "", normalized)
        if not normalized:
            raise ValueError("Intent signal names must contain letters or numbers")
        return normalized
