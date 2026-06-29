"""Adapters between Brand models and domain-neutral Core contracts."""

from dataclasses import replace

from project_origin.brand.intent.adapter import BrandIntentAdapter
from project_origin.brand.models import BrandKnowledge, FounderProfile
from project_origin.brand.naming.candidate import NameCandidate
from project_origin.core import (
    DecisionOption,
    IntentProfile,
    KnowledgeItem,
    KnowledgePacket,
)


class BrandDecisionAdapters:
    @staticmethod
    def to_intent_profile(profile: FounderProfile) -> IntentProfile:
        intent = BrandIntentAdapter.to_intent_profile(profile)
        return replace(
            intent,
            objective=(
                f"Select a strategically aligned brand name for "
                f"{profile.audience}."
            ),
        )

    @staticmethod
    def to_knowledge_packet(knowledge: BrandKnowledge) -> KnowledgePacket:
        items = (
            KnowledgeItem(
                content=knowledge.purpose,
                source="brand_knowledge.purpose",
            ),
            KnowledgeItem(
                content=knowledge.identity,
                source="brand_knowledge.identity",
            ),
            KnowledgeItem(
                content=knowledge.market_position,
                source="brand_knowledge.market_position",
            ),
            KnowledgeItem(
                content=knowledge.competitive_advantage,
                source="brand_knowledge.competitive_advantage",
            ),
        )
        return KnowledgePacket(
            domain="brand",
            query="Select the strongest brand naming direction.",
            items=items,
            metadata={
                "identity_keywords": tuple(knowledge.identity_keywords),
                "personality": knowledge.personality,
            },
        )

    @staticmethod
    def to_decision_option(candidate: NameCandidate) -> DecisionOption:
        strengths = BrandDecisionAdapters._candidate_strengths(candidate)
        weaknesses = BrandDecisionAdapters._candidate_weaknesses(candidate)

        return DecisionOption(
            identifier=candidate.name.casefold(),
            label=candidate.name,
            description=candidate.evaluation_reason,
            scores={
                "pronunciation": candidate.pronunciation_score,
                "originality": candidate.originality_score,
                "strategic_fit": candidate.strategy_score,
                "memorability": candidate.memorability_score,
                "total": candidate.total_score,
            },
            strengths=strengths,
            weaknesses=weaknesses,
            metadata={
                "style": candidate.style,
                "source": candidate.source,
                "length": candidate.length,
                **candidate.metadata,
            },
        )

    @staticmethod
    def _candidate_strengths(candidate: NameCandidate) -> tuple[str, ...]:
        score_labels = {
            "pronunciation": candidate.pronunciation_score,
            "originality": candidate.originality_score,
            "strategic fit": candidate.strategy_score,
            "memorability": candidate.memorability_score,
        }
        return tuple(
            f"Strong {label} score ({score}/10)"
            for label, score in score_labels.items()
            if score >= 8.0
        )

    @staticmethod
    def _candidate_weaknesses(candidate: NameCandidate) -> tuple[str, ...]:
        score_labels = {
            "pronunciation": candidate.pronunciation_score,
            "originality": candidate.originality_score,
            "strategic fit": candidate.strategy_score,
            "memorability": candidate.memorability_score,
        }
        return tuple(
            f"Needs review for {label} ({score}/10)"
            for label, score in score_labels.items()
            if score < 7.0
        )
