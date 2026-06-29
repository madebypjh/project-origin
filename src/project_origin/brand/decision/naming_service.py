"""Deterministic, explainable selection of evaluated brand name candidates."""

from project_origin.brand.decision.adapters import BrandDecisionAdapters
from project_origin.brand.decision.models import BrandNamingDecisionRecord
from project_origin.brand.models import BrandKnowledge, FounderProfile
from project_origin.brand.naming.candidate import NameCandidate
from project_origin.core import DecisionResult, ReasoningStep, ReasoningTrace


class NamingDecisionService:
    EXTERNAL_REVIEW_WARNINGS = (
        "Domain availability has not been checked.",
        "Trademark availability has not been checked.",
        "Multilingual and cultural risk has not been checked.",
    )

    @classmethod
    def decide(
        cls,
        profile: FounderProfile,
        knowledge: BrandKnowledge,
        candidates: list[NameCandidate],
    ) -> BrandNamingDecisionRecord:
        cls._validate_candidates(candidates)

        intent = BrandDecisionAdapters.to_intent_profile(profile)
        knowledge_packet = BrandDecisionAdapters.to_knowledge_packet(knowledge)
        ranked_candidates = sorted(
            candidates,
            key=cls._ranking_key,
        )
        options = tuple(
            BrandDecisionAdapters.to_decision_option(candidate)
            for candidate in ranked_candidates
        )
        selected = ranked_candidates[0]
        runner_up = ranked_candidates[1] if len(ranked_candidates) > 1 else None
        margin = (
            round(selected.total_score - runner_up.total_score, 2)
            if runner_up
            else None
        )

        trace = ReasoningTrace(
            steps=(
                ReasoningStep(
                    claim=f"{selected.name} has the strongest rule-based score.",
                    rationale=(
                        f"It ranked first among {len(ranked_candidates)} "
                        "evaluated candidates using the Brand naming rubric."
                    ),
                    evidence=(
                        "candidate.scores",
                        "brand_language.semantic_direction",
                    ),
                    confidence=cls._score_confidence(selected.total_score),
                ),
                ReasoningStep(
                    claim="The selection reflects the founder's stated intent.",
                    rationale=(
                        f"The objective targets {profile.audience}, while the "
                        f"decision preserves the principle: {profile.principles}"
                    ),
                    evidence=(
                        "founder_profile.audience",
                        "founder_profile.principles",
                        "brand_knowledge.identity",
                    ),
                ),
            ),
            assumptions=(
                "Internal scores are proxies for real customer perception.",
                "All candidates were evaluated with the same scoring rubric.",
            ),
            uncertainties=cls.EXTERNAL_REVIEW_WARNINGS,
        )
        rationale = cls._build_rationale(selected, runner_up, margin)
        result = DecisionResult(
            selected_option_id=selected.name.casefold(),
            options=options,
            rationale=rationale,
            trace=trace,
            confidence=cls._score_confidence(selected.total_score),
            warnings=cls.EXTERNAL_REVIEW_WARNINGS,
        )

        return BrandNamingDecisionRecord(
            intent=intent,
            knowledge=knowledge_packet,
            result=result,
        )

    @staticmethod
    def _ranking_key(candidate: NameCandidate) -> tuple[float, float, float, str]:
        return (
            -candidate.total_score,
            -candidate.strategy_score,
            -candidate.originality_score,
            candidate.name.casefold(),
        )

    @staticmethod
    def _score_confidence(total_score: float) -> float:
        # Rule-based scores cannot justify high epistemic confidence before
        # trademark, language, and customer validation.
        return round(min(total_score / 10.0, 0.8), 2)

    @staticmethod
    def _build_rationale(
        selected: NameCandidate,
        runner_up: NameCandidate | None,
        margin: float | None,
    ) -> str:
        rationale = (
            f"{selected.name} ranked first with a total score of "
            f"{selected.total_score}/10 and strategic fit of "
            f"{selected.strategy_score}/10."
        )
        if runner_up is not None and margin is not None:
            rationale += (
                f" It leads {runner_up.name} by {margin} points under the "
                "current rule-based rubric."
            )
        return rationale

    @staticmethod
    def _validate_candidates(candidates: list[NameCandidate]) -> None:
        if not candidates:
            raise ValueError("candidates must contain at least one evaluated name")

        identifiers = [candidate.name.casefold() for candidate in candidates]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("candidate names must be unique")

        for candidate in candidates:
            scores = (
                candidate.pronunciation_score,
                candidate.originality_score,
                candidate.strategy_score,
                candidate.memorability_score,
                candidate.total_score,
            )
            if any(score < 0 or score > 10 for score in scores):
                raise ValueError("candidate scores must be between 0 and 10")
            if not candidate.evaluation_reason:
                raise ValueError("candidates must be evaluated before selection")
