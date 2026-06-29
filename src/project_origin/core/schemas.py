"""Domain-neutral decision contracts.

These models describe information that every Project Origin domain may exchange.
They intentionally contain no prompting, provider, or Brand-specific behavior.
"""

from dataclasses import dataclass, field
from typing import Any


def _validate_confidence(value: float | None) -> None:
    if value is not None and not 0.0 <= value <= 1.0:
        raise ValueError("confidence must be between 0.0 and 1.0")


@dataclass(frozen=True)
class IntentProfile:
    domain: str
    objective: str
    constraints: tuple[str, ...] = ()
    preferences: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class KnowledgeItem:
    content: str
    source: str
    confidence: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_confidence(self.confidence)


@dataclass(frozen=True)
class KnowledgePacket:
    domain: str
    items: tuple[KnowledgeItem, ...]
    query: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ReasoningStep:
    claim: str
    rationale: str
    evidence: tuple[str, ...] = ()
    confidence: float | None = None

    def __post_init__(self) -> None:
        _validate_confidence(self.confidence)


@dataclass(frozen=True)
class ReasoningTrace:
    steps: tuple[ReasoningStep, ...]
    assumptions: tuple[str, ...] = ()
    uncertainties: tuple[str, ...] = ()


@dataclass(frozen=True)
class DecisionOption:
    identifier: str
    label: str
    description: str = ""
    scores: dict[str, float] = field(default_factory=dict)
    strengths: tuple[str, ...] = ()
    weaknesses: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DecisionResult:
    selected_option_id: str
    options: tuple[DecisionOption, ...]
    rationale: str
    trace: ReasoningTrace
    confidence: float | None = None
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _validate_confidence(self.confidence)
        option_ids = {option.identifier for option in self.options}
        if self.selected_option_id not in option_ids:
            raise ValueError("selected_option_id must reference one of options")
