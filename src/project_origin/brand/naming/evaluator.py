"""
Project Origin - Name Evaluator

Evaluates generated brand name candidates using rule-based scoring.
"""

from dataclasses import replace

from project_origin.brand.models import BrandLanguage
from project_origin.brand.naming.candidate import NameCandidate
from project_origin.brand.naming.generation_rules import GenerationRules
from project_origin.brand.naming.phonetics import PhoneticRules


class NameEvaluator:
    @classmethod
    def evaluate(
        cls,
        candidates: list[NameCandidate],
        brand_language: BrandLanguage,
        rules: GenerationRules | None = None,
    ) -> list[NameCandidate]:
        evaluated_names = []

        for candidate in candidates:
            evaluated_names.append(
                cls._evaluate_single_name(candidate, brand_language, rules)
            )

        return evaluated_names

    @classmethod
    def _evaluate_single_name(
        cls,
        candidate: NameCandidate,
        brand_language: BrandLanguage,
        rules: GenerationRules | None = None,
    ) -> NameCandidate:
        name = candidate.name
        pronunciation_score = cls._score_pronunciation(name)
        originality_score = cls._score_originality(name)
        strategy_score = cls._score_strategy_fit(name, brand_language)
        memorability_score = cls._score_memorability(name)

        base_score = (
            pronunciation_score * 0.25
            + originality_score * 0.25
            + strategy_score * 0.30
            + memorability_score * 0.20
        )
        knowledge_score = None
        guidance_strength = 0.0

        if rules is not None and rules.guidance_strength > 0:
            knowledge_score = cls._score_generation_rules_fit(name, rules)
            guidance_strength = rules.guidance_strength

        if knowledge_score is None:
            total_score = round(base_score, 2)
        else:
            total_score = round(
                base_score * (1 - guidance_strength)
                + knowledge_score * guidance_strength,
                2,
            )

        reason = (
            f"{name} scored {total_score}/10 based on pronunciation, "
            f"originality, strategic fit, and memorability."
        )
        if knowledge_score is not None and rules is not None:
            reason += (
                f" Naming knowledge contributed weakly "
                f"({rules.recommended_usage}, {knowledge_score}/10)."
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

    @classmethod
    def _score_generation_rules_fit(
        cls,
        name: str,
        rules: GenerationRules,
    ) -> float:
        letters = [character for character in name.lower() if character.isalpha()]
        if not letters:
            return 5.0

        length_score = cls._clamp(
            10 - abs(len(letters) - rules.target_length) * 1.5,
            minimum=4.0,
        )
        vowel_ratio = cls._ratio(letters, "aeiou")
        hard_ratio = cls._ratio(letters, "bcdfgkpqtxz")
        soft_ratio = cls._ratio(letters, "hjklmnrsfvwyl")

        vowel_score = cls._clamp(
            10 - abs(vowel_ratio - rules.target_vowel_ratio) * 10,
            minimum=4.0,
        )
        hard_score = cls._clamp(
            10 - abs(hard_ratio - rules.target_hard_consonant_ratio) * 10,
            minimum=4.0,
        )
        soft_score = cls._clamp(
            10 - abs(soft_ratio - rules.target_soft_consonant_ratio) * 10,
            minimum=4.0,
        )

        return round(
            (length_score + vowel_score + hard_score + soft_score) / 4,
            2,
        )

    @staticmethod
    def _ratio(letters: list[str], matches: str) -> float:
        if not letters:
            return 0.0

        return sum(1 for letter in letters if letter in matches) / len(letters)

    @staticmethod
    def _clamp(
        value: float,
        minimum: float = 0.0,
        maximum: float = 10.0,
    ) -> float:
        return max(minimum, min(maximum, value))
