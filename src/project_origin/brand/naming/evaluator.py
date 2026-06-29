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
            pronunciation_score * 0.12
            + originality_score * 0.14
            + strategy_score * 0.65
            + memorability_score * 0.09
        )
        decision_adjustment = cls._score_decision_separation_adjustment(
            strategy_score,
        )
        adjusted_base_score = cls._clamp(base_score + decision_adjustment)
        knowledge_score = None
        guidance_strength = 0.0

        if rules is not None and rules.guidance_strength > 0:
            knowledge_score = cls._score_generation_rules_fit(name, rules)
            guidance_strength = rules.guidance_strength

        if knowledge_score is None:
            total_score = round(adjusted_base_score, 2)
        else:
            total_score = round(
                adjusted_base_score * (1 - guidance_strength)
                + knowledge_score * guidance_strength,
                2,
            )
        evaluation_breakdown = cls._build_evaluation_breakdown(
            pronunciation_score=pronunciation_score,
            originality_score=originality_score,
            strategy_score=strategy_score,
            memorability_score=memorability_score,
            base_score=base_score,
            decision_adjustment=decision_adjustment,
            total_score=total_score,
            rules=rules,
            knowledge_score=knowledge_score,
            guidance_strength=guidance_strength,
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
            metadata={
                **candidate.metadata,
                "evaluation_breakdown": evaluation_breakdown,
            },
        )

    @staticmethod
    def _score_pronunciation(name: str) -> float:
        if not PhoneticRules.is_pronounceable(name):
            return 3.0

        letters = [character for character in name.lower() if character.isalpha()]
        length = len(letters)
        vowel_ratio = NameEvaluator._ratio(letters, "aeiou")
        score = 8.8

        if 5 <= length <= 8:
            score += 0.4
        elif 4 <= length <= 10:
            score += 0.1
        else:
            score -= 1.0

        if 0.32 <= vowel_ratio <= 0.55:
            score += 0.3
        elif vowel_ratio < 0.25 or vowel_ratio > 0.68:
            score -= 0.9

        if NameEvaluator._has_awkward_cluster(name):
            score -= 0.6

        return round(NameEvaluator._clamp(score, minimum=3.0), 2)

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

        score = 7.6
        for fragment in generic_fragments:
            if fragment in lower_name:
                score -= 1.4

        letters = [character for character in lower_name if character.isalpha()]
        unique_letter_ratio = NameEvaluator._unique_ratio(letters)

        if 5 <= len(lower_name) <= 8:
            score += 0.5
        elif len(lower_name) <= 4:
            score += 0.2
        elif len(lower_name) > 10:
            score -= 0.4

        ending_adjustments = {
            "io": -0.22,
            "ia": -0.16,
            "on": -0.10,
            "a": -0.08,
            "is": -0.05,
            "axis": 0.12,
            "scope": 0.10,
            "core": 0.04,
        }
        for ending, adjustment in ending_adjustments.items():
            if lower_name.endswith(ending):
                score += adjustment
                break

        if NameEvaluator._has_repeated_chunk(lower_name):
            score -= 0.8

        if unique_letter_ratio >= 0.78:
            score += 0.25
        elif unique_letter_ratio >= 0.65:
            score += 0.12
        elif unique_letter_ratio < 0.45:
            score -= 0.25

        uncommon_letters = sum(
            1 for letter in lower_name if letter in {"v", "x", "z", "q"}
        )
        score += min(uncommon_letters * 0.15, 0.45)

        return round(NameEvaluator._clamp(score, minimum=4.0), 2)

    @staticmethod
    def _score_strategy_fit(
        name: str,
        brand_language: BrandLanguage,
    ) -> float:
        lower_name = name.lower()

        score = 6.4
        seen_roots = set()

        for word in brand_language.vocabulary:
            normalized_word = word.lower().strip()
            if len(normalized_word) < 3:
                continue

            root = normalized_word[:4]
            if root in seen_roots:
                continue
            seen_roots.add(root)

            if normalized_word in lower_name:
                score += 1.35
            elif len(normalized_word) >= 5 and normalized_word[:5] in lower_name:
                score += 1.10
            elif normalized_word[:4] in lower_name:
                score += 0.80
            elif normalized_word[:3] in lower_name:
                score += 0.50

        semantic_tokens = [
            token
            for token in brand_language.semantic_direction.lower().replace(
                ",",
                " ",
            ).replace(
                ".",
                " ",
            ).split()
            if len(token) >= 4
        ]
        for token in dict.fromkeys(semantic_tokens[:12]):
            if token[:4] in lower_name:
                score += 0.30

        if brand_language.style and brand_language.style.lower() in lower_name:
            score += 0.2

        return round(NameEvaluator._clamp(score, minimum=5.0, maximum=9.6), 2)

    @staticmethod
    def _score_memorability(name: str) -> float:
        letters = [character for character in name.lower() if character.isalpha()]
        length = len(letters)
        vowel_ratio = NameEvaluator._ratio(letters, "aeiou")
        score = 7.0

        if 5 <= length <= 7:
            score += 1.4
        elif 8 <= length <= 10:
            score += 0.8
        elif length == 4:
            score += 0.5
        else:
            score -= 0.2

        if 0.34 <= vowel_ratio <= 0.55:
            score += 0.5
        elif vowel_ratio < 0.25 or vowel_ratio > 0.65:
            score -= 0.5

        if NameEvaluator._has_repeated_chunk(name.lower()):
            score -= 0.6

        if NameEvaluator._has_balanced_rhythm(letters):
            score += 0.4

        return round(NameEvaluator._clamp(score, minimum=5.0), 2)

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
    def _build_evaluation_breakdown(
        pronunciation_score: float,
        originality_score: float,
        strategy_score: float,
        memorability_score: float,
        base_score: float,
        decision_adjustment: float,
        total_score: float,
        rules: GenerationRules | None,
        knowledge_score: float | None,
        guidance_strength: float,
    ) -> dict:
        breakdown = {
            "version": "brand_naming_evaluation_v1",
            "components": {
                "pronunciation": {
                    "score": pronunciation_score,
                    "weight": 0.12,
                },
                "originality": {
                    "score": originality_score,
                    "weight": 0.14,
                },
                "strategic_fit": {
                    "score": strategy_score,
                    "weight": 0.65,
                },
                "memorability": {
                    "score": memorability_score,
                    "weight": 0.09,
                },
            },
            "base_score": round(base_score, 2),
            "decision_separation_adjustment": decision_adjustment,
            "total_score": total_score,
            "knowledge_guidance": {
                "applied": False,
                "score": None,
                "usage": None,
                "strength": 0.0,
                "confidence": None,
                "sample_size": 0,
            },
        }

        if rules is not None:
            breakdown["knowledge_guidance"] = {
                "applied": knowledge_score is not None,
                "score": knowledge_score,
                "usage": rules.recommended_usage,
                "strength": guidance_strength,
                "confidence": rules.knowledge_confidence,
                "sample_size": rules.sample_size,
            }

        return breakdown

    @staticmethod
    def _ratio(letters: list[str], matches: str) -> float:
        if not letters:
            return 0.0

        return sum(1 for letter in letters if letter in matches) / len(letters)

    @staticmethod
    def _score_decision_separation_adjustment(strategy_score: float) -> float:
        if strategy_score >= 8.5:
            return 0.14
        if strategy_score >= 8.25:
            return 0.10
        if strategy_score >= 8.0:
            return 0.06
        if strategy_score < 7.5:
            return -0.06
        return 0.0

    @staticmethod
    def _unique_ratio(letters: list[str]) -> float:
        if not letters:
            return 0.0

        return len(set(letters)) / len(letters)

    @staticmethod
    def _has_awkward_cluster(name: str) -> bool:
        lower_name = name.lower()
        consonant_cluster = 0
        for character in lower_name:
            if character.isalpha() and character not in "aeiou":
                consonant_cluster += 1
                if consonant_cluster >= 4:
                    return True
            else:
                consonant_cluster = 0
        return False

    @staticmethod
    def _has_repeated_chunk(name: str) -> bool:
        for size in (2, 3):
            for index in range(len(name) - size * 2 + 1):
                chunk = name[index:index + size]
                if chunk and chunk == name[index + size:index + size * 2]:
                    return True
        return False

    @staticmethod
    def _has_balanced_rhythm(letters: list[str]) -> bool:
        if len(letters) < 5:
            return False

        transitions = 0
        previous_is_vowel = letters[0] in "aeiou"
        for letter in letters[1:]:
            is_vowel = letter in "aeiou"
            if is_vowel != previous_is_vowel:
                transitions += 1
            previous_is_vowel = is_vowel

        return transitions >= max(3, len(letters) // 2)

    @staticmethod
    def _clamp(
        value: float,
        minimum: float = 0.0,
        maximum: float = 10.0,
    ) -> float:
        return max(minimum, min(maximum, value))
