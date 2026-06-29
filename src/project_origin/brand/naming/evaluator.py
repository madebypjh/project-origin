"""
Project Origin - Name Evaluator

Evaluates generated brand name candidates using rule-based scoring.
"""

from dataclasses import replace

from project_origin.brand.models import BrandLanguage
from project_origin.brand.naming.candidate import NameCandidate
from project_origin.brand.naming.phonetics import PhoneticRules


class NameEvaluator:
    @classmethod
    def evaluate(
        cls,
        candidates: list[NameCandidate],
        brand_language: BrandLanguage,
    ) -> list[NameCandidate]:
        evaluated_names = []

        for candidate in candidates:
            evaluated_names.append(
                cls._evaluate_single_name(candidate, brand_language)
            )

        return evaluated_names

    @classmethod
    def _evaluate_single_name(
        cls,
        candidate: NameCandidate,
        brand_language: BrandLanguage,
    ) -> NameCandidate:
        name = candidate.name
        pronunciation_score = cls._score_pronunciation(name)
        originality_score = cls._score_originality(name)
        strategy_score = cls._score_strategy_fit(name, brand_language)
        memorability_score = cls._score_memorability(name)

        total_score = round(
            (
                pronunciation_score * 0.25
                + originality_score * 0.25
                + strategy_score * 0.30
                + memorability_score * 0.20
            ),
            2,
        )

        reason = (
            f"{name} scored {total_score}/10 based on pronunciation, "
            f"originality, strategic fit, and memorability."
        )

        return replace(
            candidate,
            pronunciation_score=pronunciation_score,
            originality_score=originality_score,
            strategy_score=strategy_score,
            memorability_score=memorability_score,
            total_score=total_score,
            evaluation_reason=reason,
        )

    @staticmethod
    def _score_pronunciation(name: str) -> float:
        if not PhoneticRules.is_pronounceable(name):
            return 3.0

        length = len(name)

        if 5 <= length <= 8:
            return 9.0

        if 4 <= length <= 10:
            return 7.5

        return 6.0

    @staticmethod
    def _score_originality(name: str) -> float:
        lower_name = name.lower()

        generic_fragments = [
            "brand",
            "name",
            "ai",
            "tech",
            "labs",
            "group",
            "company",
            "consulting",
        ]

        if any(fragment in lower_name for fragment in generic_fragments):
            return 5.0

        if len(lower_name) <= 5:
            return 8.5

        return 7.5

    @staticmethod
    def _score_strategy_fit(
        name: str,
        brand_language: BrandLanguage,
    ) -> float:
        lower_name = name.lower()

        matched_words = [
            word for word in brand_language.vocabulary
            if word.lower()[:3] in lower_name
        ]

        if len(matched_words) >= 2:
            return 9.0

        if len(matched_words) == 1:
            return 7.5

        return 6.0

    @staticmethod
    def _score_memorability(name: str) -> float:
        length = len(name)

        if 5 <= length <= 7:
            return 9.0

        if 8 <= length <= 10:
            return 7.5

        return 6.5
