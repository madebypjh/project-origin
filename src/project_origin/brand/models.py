"""
Project Origin - Brand Domain Models
"""

from dataclasses import dataclass, asdict, field
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
class NameRecommendation:
    name: str
    meaning: str
    strategic_fit: str
    strengths: str
    weaknesses: str
    score: float
    score_reason: str


@dataclass
class BrandDNAItem:
    principle: str
    meaning: str
    how_it_shows_up: str


@dataclass
class StrategicValueItem:
    value: str
    strategic_role: str
    decision_rule: str


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

    name_recommendations: list[NameRecommendation]

    final_recommendation: str

    brand_origin_story: str = ""

    brand_dna: str = ""

    strategic_values: str = ""

    selected_name_rationale: str = ""

    candidate_comparison: str = ""

    strategic_risks: str = ""

    next_action_plan: str = ""

    brand_dna_items: list[BrandDNAItem] = field(default_factory=list)

    strategic_value_items: list[StrategicValueItem] = field(default_factory=list)

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

