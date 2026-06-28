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
    purpose: str
    method: str
    offering: str
    identity: str
    personality: str
    core_values: list[str]
    target_customer: str
    market_position: str
    competitive_advantage: str
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

@dataclass
class SemanticProfile:
    themes: dict[str, float]
    keywords: list[str]
    vocabulary: list[str]
    dominant_theme: str

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

@dataclass
class BrandLanguage:
    vocabulary: list[str]
    tone: str
    emotion: str
    style: str
    semantic_direction: str

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)