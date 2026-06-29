"""
Project Origin - Candidate Name Model

Represents a generated brand name with measurable linguistic attributes.
"""

from dataclasses import dataclass, asdict
import json


@dataclass
class CandidateName:
    name: str
    length: int
    syllable_count: int
    style: str
    vowel_ratio: float
    hard_consonant_ratio: float
    soft_consonant_ratio: float
    source: str = "generator_v2"
    rule_score: float = 0.0
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)