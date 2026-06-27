"""
Project Origin - Brand Strategy Frameworks

This module contains framework-based reasoning logic used by KnowledgeBuilder.
"""

from .models import FounderProfile


class GoldenCircleFramework:
    @staticmethod
    def analyze(profile: FounderProfile) -> dict:
        return {
            "why": f"Help {profile.audience} solve the problem of {profile.problem}.",
            "how": f"Use {profile.differentiation} while protecting {profile.principles}.",
            "what": "Deliver an AI-generated Brand Strategy Report."
        }


class BrandDNAFramework:
    @staticmethod
    def analyze(profile: FounderProfile) -> dict:
        return {
            "identity": (
                f"A brand strategy intelligence system for {profile.audience}, "
                f"focused on solving {profile.problem}."
            ),
            "core_values": [
                profile.principles,
                "Clarity",
                "Trust",
                "Strategic Reasoning",
                "Long-term Value"
            ],
            "personality": ArchetypeFramework.analyze(profile)["primary_archetype"]
        }


class PositioningFramework:
    @staticmethod
    def analyze(profile: FounderProfile) -> dict:
        return {
            "target_customer": profile.audience,
            "market_position": "AI Brand Strategy Consultant",
            "competitive_advantage": (
                f"Unlike generic naming tools, Project Origin connects branding decisions "
                f"with founder intent, long-term vision, and {profile.differentiation}."
            ),
        }


class ArchetypeFramework:
    @staticmethod
    def analyze(profile: FounderProfile) -> dict:
        text = " ".join([
            profile.problem,
            profile.audience,
            profile.vision,
            profile.principles,
            profile.differentiation,
        ]).lower()

        if any(word in text for word in ["ai", "인공지능", "사고", "추론", "분석", "지능"]):
            archetype = "Sage + Creator"
            reason = "The brand emphasizes intelligence, reasoning, creation, and strategic thinking."
        elif any(word in text for word in ["보안", "취약점", "스캔", "위협", "security"]):
            archetype = "Sage + Hero"
            reason = "The brand emphasizes protection, expertise, and problem-solving."
        elif any(word in text for word in ["발견", "탐색", "recon", "osint", "discovery"]):
            archetype = "Explorer + Sage"
            reason = "The brand emphasizes discovery, exploration, and intelligence."
        else:
            archetype = "Sage"
            reason = "The brand emphasizes insight, clarity, and decision-making."

        return {
            "primary_archetype": archetype,
            "reason": reason,
        }


class ValuePropositionFramework:
    @staticmethod
    def analyze(profile: FounderProfile) -> dict:
        return {
            "customer_problem": profile.problem,
            "customer_value": (
                "Customers gain clearer strategic direction and stronger confidence "
                "in branding decisions."
            ),
            "solution": (
                f"Project Origin uses {profile.differentiation} to transform founder input "
                "into a professional Brand Strategy Report."
            ),
        }


class NamingEvaluationFramework:
    @staticmethod
    def criteria() -> list[str]:
        return [
            "Meaning",
            "Memorability",
            "Pronunciation",
            "Strategic Alignment",
            "Scalability",
            "Emotional Impact",
            "Founder Intent Fit",
        ]