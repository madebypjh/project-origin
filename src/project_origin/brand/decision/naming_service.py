"""Deterministic, explainable selection of evaluated brand name candidates."""

from project_origin.brand.decision.adapters import BrandDecisionAdapters
from project_origin.brand.decision.models import (
    BrandNamingDecisionEvidence,
    BrandNamingDecisionRecord,
)
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
        evidence = cls._build_decision_evidence(
            profile=profile,
            knowledge=knowledge,
            selected=selected,
            runner_up=runner_up,
            margin=margin,
        )

        trace = ReasoningTrace(
            steps=(
                ReasoningStep(
                    claim=f"{selected.name} has the strongest decision evidence.",
                    rationale=(
                        cls._evidence_rationale(evidence)
                    ),
                    evidence=(
                        "candidate.scores",
                        "candidate.generation_metadata",
                        "brand_language.semantic_direction",
                    ),
                    confidence=cls._score_confidence(selected.total_score),
                ),
                ReasoningStep(
                    claim="The selection can feed a consultant-grade brand report.",
                    rationale=(
                        f"The decision preserves DNA cues ({', '.join(evidence.brand_dna)}) "
                        f"and value alignment ({', '.join(evidence.value_alignment)})."
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
        rationale = cls._build_rationale(evidence)
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
            evidence=evidence,
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

    @classmethod
    def _build_rationale(
        cls,
        evidence: BrandNamingDecisionEvidence,
    ) -> str:
        rationale = (
            f"{evidence.selected_name} is recommended because it has the "
            f"strongest combined naming evidence: "
            f"{'; '.join(evidence.selected_advantages)}."
        )
        if evidence.runner_up_name is not None and evidence.score_delta is not None:
            rationale += (
                f" It leads {evidence.runner_up_name} by "
                f"{evidence.score_delta} total-score points"
            )
            if evidence.strategy_delta is not None:
                rationale += (
                    f" and {evidence.strategy_delta} strategic-fit points"
                )
            rationale += "."
        rationale += (
            " Structured report evidence is available for brand history, "
            "DNA, value alignment, and downstream consultant-grade reporting."
        )
        return rationale

    @classmethod
    def _build_decision_evidence(
        cls,
        profile: FounderProfile,
        knowledge: BrandKnowledge,
        selected: NameCandidate,
        runner_up: NameCandidate | None,
        margin: float | None,
    ) -> BrandNamingDecisionEvidence:
        strategy_delta = cls._score_delta(
            selected.strategy_score,
            runner_up.strategy_score if runner_up else None,
        )
        originality_delta = cls._score_delta(
            selected.originality_score,
            runner_up.originality_score if runner_up else None,
        )
        memorability_delta = cls._score_delta(
            selected.memorability_score,
            runner_up.memorability_score if runner_up else None,
        )

        selected_advantages = cls._selected_advantages(
            selected,
            runner_up,
            margin,
            strategy_delta,
        )
        runner_up_tradeoffs = cls._runner_up_tradeoffs(
            selected,
            runner_up,
            originality_delta,
            memorability_delta,
        )
        brand_dna = tuple(dict.fromkeys(
            [
                *knowledge.core_values[:3],
                knowledge.personality,
            ]
        ))
        value_alignment = tuple(dict.fromkeys(
            [
                profile.principles,
                profile.differentiation,
                knowledge.competitive_advantage,
            ]
        ))

        return BrandNamingDecisionEvidence(
            selected_name=selected.name,
            runner_up_name=runner_up.name if runner_up else None,
            score_delta=margin,
            strategy_delta=strategy_delta,
            originality_delta=originality_delta,
            memorability_delta=memorability_delta,
            selected_advantages=selected_advantages,
            runner_up_tradeoffs=runner_up_tradeoffs,
            risk_assessment=(
                "No domain, trademark, or multilingual screening has been performed.",
                "Internal scoring is a strategic proxy, not market validation.",
            ),
            brand_history_seed=(
                f"The brand should grow from the founder's original problem: "
                f"{profile.problem} Its narrative points toward: {profile.vision}"
            ),
            brand_dna=brand_dna,
            value_alignment=value_alignment,
        )

    @staticmethod
    def _score_delta(
        selected_score: float,
        runner_up_score: float | None,
    ) -> float | None:
        if runner_up_score is None:
            return None
        return round(selected_score - runner_up_score, 2)

    @staticmethod
    def _selected_advantages(
        selected: NameCandidate,
        runner_up: NameCandidate | None,
        margin: float | None,
        strategy_delta: float | None,
    ) -> tuple[str, ...]:
        advantages = [
            f"total score {selected.total_score}/10",
            f"strategic fit {selected.strategy_score}/10",
        ]
        pattern = selected.metadata.get("generation_pattern")
        if pattern:
            advantages.append(f"generated through {pattern}")
        if margin is not None and margin >= 0.15:
            advantages.append(f"clear score margin of {margin}")
        if strategy_delta is not None and strategy_delta > 0:
            advantages.append(
                f"stronger strategy signal than {runner_up.name}"
            )
        return tuple(advantages)

    @staticmethod
    def _runner_up_tradeoffs(
        selected: NameCandidate,
        runner_up: NameCandidate | None,
        originality_delta: float | None,
        memorability_delta: float | None,
    ) -> tuple[str, ...]:
        if runner_up is None:
            return ()

        tradeoffs = [
            f"{runner_up.name} scored {runner_up.total_score}/10 overall",
        ]
        if runner_up.strategy_score < selected.strategy_score:
            tradeoffs.append(
                f"weaker strategic fit ({runner_up.strategy_score}/10)"
            )
        if originality_delta is not None and originality_delta < 0:
            tradeoffs.append(
                f"more original by {abs(originality_delta)} points"
            )
        if memorability_delta is not None and memorability_delta < 0:
            tradeoffs.append(
                f"more memorable by {abs(memorability_delta)} points"
            )
        return tuple(tradeoffs)

    @staticmethod
    def _evidence_rationale(
        evidence: BrandNamingDecisionEvidence,
    ) -> str:
        rationale = "; ".join(evidence.selected_advantages)
        if evidence.runner_up_tradeoffs:
            rationale += (
                ". Runner-up tradeoffs: "
                + "; ".join(evidence.runner_up_tradeoffs)
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
