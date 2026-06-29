"""
Project Origin - Candidate Name Model

Represents a brand name throughout generation, filtering, evaluation, and ranking.
"""

from dataclasses import asdict, dataclass, field
import json
from typing import Any


@dataclass
class NameCandidate:
    name: str
    style: str = ""
    source: str = "generator_v2"
    syllable_count: int | None = None
    rule_score: float = 0.0
    pronunciation_score: float = 0.0
    originality_score: float = 0.0
    strategy_score: float = 0.0
    memorability_score: float = 0.0
    total_score: float = 0.0
    evaluation_reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def length(self) -> int:
        return len(self.name)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
