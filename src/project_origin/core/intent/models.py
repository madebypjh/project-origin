"""Structured, evidence-backed representations of human intent."""

from dataclasses import dataclass, field
from typing import Any


def _validate_probability(value: float, field_name: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{field_name} must be between 0.0 and 1.0")


@dataclass(frozen=True)
class IntentSignal:
    kind: str
    concept: str
    weight: float
    evidence: tuple[str, ...]
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.kind.strip():
            raise ValueError("IntentSignal kind must not be empty")
        if not self.concept.strip():
            raise ValueError("IntentSignal concept must not be empty")
        if not self.evidence:
            raise ValueError("IntentSignal evidence must not be empty")
        if any(not item.strip() for item in self.evidence):
            raise ValueError("IntentSignal evidence items must not be empty")
        _validate_probability(self.weight, "IntentSignal weight")
        _validate_probability(self.confidence, "IntentSignal confidence")


@dataclass(frozen=True)
class IntentProfile:
    domain: str
    objective: str
    constraints: tuple[str, ...] = ()
    preferences: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    signals: tuple[IntentSignal, ...] = ()
    unresolved_signals: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.domain.strip():
            raise ValueError("IntentProfile domain must not be empty")
        if not self.objective.strip():
            raise ValueError("IntentProfile objective must not be empty")
