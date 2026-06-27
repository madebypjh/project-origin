"""
Project Origin - Knowledge Builder v2

Transforms FounderProfile into structured BrandKnowledge
using brand strategy frameworks.
"""

from .models import FounderProfile, BrandKnowledge


class KnowledgeBuilder:
    @staticmethod
    def build(profile: FounderProfile) -> BrandKnowledge:
        purpose, method, offering = KnowledgeBuilder._build_golden_circle(profile)
        identity, personality, core_values = KnowledgeBuilder._build_brand_dna(profile)
        market_position, competitive_advantage = KnowledgeBuilder._build_positioning(profile)
        identity_keywords = KnowledgeBuilder._extract_identity_keywords(profile)

        return BrandKnowledge(
            purpose=purpose,
            method=method,
            offering=offering,
            identity=identity,
            personality=personality,
            core_values=core_values,
            target_customer=profile.audience,
            market_position=market_position,
            competitive_advantage=competitive_advantage,
            identity_keywords=identity_keywords,
        )

    @staticmethod
    def _build_golden_circle(profile: FounderProfile) -> tuple[str, str, str]:
        purpose = f"Help {profile.audience} solve the problem of {profile.problem}."
        method = f"Create value through {profile.differentiation} while protecting {profile.principles}."
        offering = "An AI-powered Brand Strategy Report that supports better branding decisions."

        return purpose, method, offering

    @staticmethod
    def _build_brand_dna(profile: FounderProfile) -> tuple[str, str, list[str]]:
        identity = (
            f"A strategic AI brand intelligence system focused on {profile.problem} "
            f"for {profile.audience}."
        )

        personality = KnowledgeBuilder._infer_archetype(profile)

        core_values = [
            profile.principles,
            "Clarity",
            "Trust",
            "Strategic Reasoning",
            "Long-term Value",
        ]

        return identity, personality, core_values

    @staticmethod
    def _build_positioning(profile: FounderProfile) -> tuple[str, str]:
        market_position = (
            "AI Brand Strategy Consultant, not a simple name generator."
        )

        competitive_advantage = (
            f"Unlike generic naming tools, this approach uses {profile.differentiation} "
            f"to connect brand decisions with the founder's mission, values, and long-term vision."
        )

        return market_position, competitive_advantage

    @staticmethod
    def _infer_archetype(profile: FounderProfile) -> str:
        text = " ".join([
            profile.problem,
            profile.audience,
            profile.vision,
            profile.principles,
            profile.differentiation,
        ]).lower()

        if any(word in text for word in ["ai", "인공지능", "사고", "분석", "지능"]):
            return "Sage + Creator"

        if any(word in text for word in ["보안", "취약점", "스캔", "위협"]):
            return "Sage + Hero"

        if any(word in text for word in ["발견", "탐색", "recon", "osint"]):
            return "Explorer + Sage"

        return "Sage"

    @staticmethod
    def _extract_identity_keywords(profile: FounderProfile) -> list[str]:
        text = " ".join([
            profile.problem,
            profile.audience,
            profile.vision,
            profile.principles,
            profile.differentiation,
        ]).lower()

        keyword_map = {
            "AI": ["ai", "인공지능", "artificial intelligence"],
            "Strategy": ["전략", "strategy"],
            "Reasoning": ["사고", "추론", "reasoning"],
            "Quality": ["품질", "퀄리티", "quality"],
            "Security": ["보안", "취약점", "스캔", "security"],
            "Discovery": ["발견", "탐색", "recon", "discovery"],
            "Trust": ["신뢰", "trust"],
            "Automation": ["자동화", "automation"],
            "Intelligence": ["지능", "intelligence"],
        }

        keywords = []

        for keyword, patterns in keyword_map.items():
            if any(pattern in text for pattern in patterns):
                keywords.append(keyword)

        if not keywords:
            keywords = ["Strategy", "Quality", "Trust"]

        return keywords