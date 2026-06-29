"""
Project Origin - Generation Rules

Converts compiled naming knowledge into generator-friendly rules.
"""

from dataclasses import dataclass, asdict
import json


@dataclass
class GenerationRules:
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

        hard_ratio = knowledge.get("recommended_hard_consonant_ratio", 0.3)
        soft_ratio = knowledge.get("recommended_soft_consonant_ratio", 0.3)

        return GenerationRules(
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