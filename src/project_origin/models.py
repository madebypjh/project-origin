"""
Project Origin - Data Models
"""

from dataclasses import dataclass, asdict
import json


@dataclass
class FounderProfile:
    problem: str
    audience: str
    vision: str
    principles: str
    differentiation: str

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


@dataclass
class BrandKnowledge:
    core_problem: str
    target_customer: str
    strategic_goal: str
    core_principles: str
    differentiation: str
    identity_keywords: list[str]

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)