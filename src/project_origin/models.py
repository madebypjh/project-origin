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

@dataclass
class BrandStrategyReport:
    executive_summary: str

    founder_insights: str

    brand_identity: str

    mission_statement: str

    vision_statement: str

    core_values: str

    positioning: str

    target_audience: str

    brand_personality: str

    naming_strategy: str

    name_recommendations: list[str]

    final_recommendation: str

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
            indent=2
        )