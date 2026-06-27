"""
Project Origin - Knowledge Builder

Converts raw FounderProfile data into structured BrandKnowledge.
"""

from .models import FounderProfile, BrandKnowledge


class KnowledgeBuilder:
    @staticmethod
    def build(profile: FounderProfile) -> BrandKnowledge:
        identity_keywords = KnowledgeBuilder._extract_keywords(profile)

        return BrandKnowledge(
            core_problem=profile.problem,
            target_customer=profile.audience,
            strategic_goal=profile.vision,
            core_principles=profile.principles,
            differentiation=profile.differentiation,
            identity_keywords=identity_keywords,
        )

    @staticmethod
    def _extract_keywords(profile: FounderProfile) -> list[str]:
        raw_text = " ".join([
            profile.problem,
            profile.audience,
            profile.vision,
            profile.principles,
            profile.differentiation,
        ])

        keyword_candidates = [
            "AI",
            "Brand",
            "Strategy",
            "Quality",
            "Trust",
            "Reasoning",
            "Automation",
            "Security",
            "Discovery",
            "Report",
            "Intelligence",
            "Clarity",
        ]

        found_keywords = []

        for keyword in keyword_candidates:
            if keyword.lower() in raw_text.lower():
                found_keywords.append(keyword)

        if not found_keywords:
            found_keywords = ["Quality", "Trust", "Reasoning"]

        return found_keywords