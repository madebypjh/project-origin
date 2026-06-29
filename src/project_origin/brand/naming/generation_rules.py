"""
Project Origin - Brand Name Generation Rules

Converts compiled naming knowledge into generator-friendly rules.
"""

from dataclasses import dataclass, asdict
import json


@dataclass
class GenerationRules:
    sample_size: int = 0
    knowledge_confidence: str = "insufficient"
    recommended_usage: str = "do_not_enforce"
    guidance_strength: float = 0.0
    preferred_style: str = "invented"
    preferred_tone: str = "balanced"
    target_length: int = 7
    target_syllables: int = 2
    target_vowel_ratio: float = 0.4
    target_hard_consonant_ratio: float = 0.3
    target_soft_consonant_ratio: float = 0.3
    prefer_hard_consonants: bool = False
    prefer_soft_consonants: bool = False
    avoid_generic_words: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class GenerationRulesBuilder:
    @staticmethod
    def build(knowledge: dict | None = None) -> GenerationRules:
        if not knowledge:
            return GenerationRules()

        sample_size = int(knowledge.get("sample_size", 0) or 0)
        recommended_usage = knowledge.get(
            "recommended_usage",
            GenerationRulesBuilder._recommended_usage(sample_size),
        )
        hard_ratio = knowledge.get("recommended_hard_consonant_ratio", 0.3)
        soft_ratio = knowledge.get("recommended_soft_consonant_ratio", 0.3)

        return GenerationRules(
            sample_size=sample_size,
            knowledge_confidence=knowledge.get(
                "knowledge_confidence",
                GenerationRulesBuilder._sample_confidence(sample_size),
            ),
            recommended_usage=recommended_usage,
            guidance_strength=GenerationRulesBuilder._guidance_strength(
                recommended_usage
            ),
            preferred_style=knowledge.get("preferred_style", "invented"),
            preferred_tone=knowledge.get("preferred_tone", "balanced"),
            target_length=knowledge.get("recommended_name_length", 7),
            target_syllables=knowledge.get("recommended_syllable_count", 2),
            target_vowel_ratio=knowledge.get("recommended_vowel_ratio", 0.4),
            target_hard_consonant_ratio=hard_ratio,
            target_soft_consonant_ratio=soft_ratio,
            prefer_hard_consonants=hard_ratio >= 0.4,
            prefer_soft_consonants=soft_ratio >= 0.4,
            avoid_generic_words=True,
        )

    @staticmethod
    def _sample_confidence(sample_size: int) -> str:
        if sample_size >= 80:
            return "high"

        if sample_size >= 30:
            return "medium"

        if sample_size >= 10:
            return "low"

        return "insufficient"

    @staticmethod
    def _recommended_usage(sample_size: int) -> str:
        if sample_size >= 80:
            return "strong_guidance"

        if sample_size >= 30:
            return "soft_guidance"

        if sample_size >= 10:
            return "weak_guidance"

        return "do_not_enforce"

    @staticmethod
    def _guidance_strength(recommended_usage: str) -> float:
        strengths = {
            "do_not_enforce": 0.0,
            "weak_guidance": 0.05,
            "soft_guidance": 0.10,
            "strong_guidance": 0.15,
        }
        return strengths.get(recommended_usage, 0.0)
