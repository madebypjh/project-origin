"""
Project Origin - Semantic Naming Generator

Generates original brand name candidates from BrandLanguage.
"""

import random

from src.project_origin.models import BrandLanguage
from src.project_origin.naming.morphology import MorphologyLibrary
from src.project_origin.naming.phonetics import PhoneticRules


class NamingGenerator:
    DEFAULT_CANDIDATE_COUNT = 100

    VOCABULARY_TO_MORPHOLOGY = {
        "intelligence": ["tech", "greek"],
        "logic": ["tech", "strategy"],
        "system": ["tech"],
        "signal": ["strategy", "tech"],
        "truth": ["trust", "latin"],
        "clarity": ["trust", "strategy"],
        "integrity": ["trust"],
        "confidence": ["trust", "premium"],
        "direction": ["strategy", "latin"],
        "alignment": ["strategy"],
        "decision": ["strategy", "tech"],
        "framework": ["strategy"],
        "quality": ["premium", "trust"],
        "precision": ["premium", "strategy"],
        "elegance": ["premium"],
        "insight": ["discovery", "strategy"],
        "origin": ["latin", "discovery"],
        "identity": ["creativity", "premium"],
        "story": ["creativity"],
        "voice": ["creativity"],
    }

    STYLE_SUFFIXES = {
        "modern": ["io", "ix", "ora", "on"],
        "clear": ["a", "ia", "is", "on"],
        "structured": ["axis", "core", "scope", "on"],
        "minimal": ["a", "el", "or", "is"],
        "open": ["ora", "via", "a", "ia"],
        "expressive": ["ora", "ia", "ella", "io"],
    }

    @classmethod
    def generate(
        cls,
        brand_language: BrandLanguage,
        count: int = DEFAULT_CANDIDATE_COUNT,
    ) -> list[str]:
        morphemes = cls._select_morphemes(brand_language)
        suffixes = cls._select_suffixes(brand_language)

        candidates = set()
        attempts = 0
        max_attempts = count * 30

        while len(candidates) < count and attempts < max_attempts:
            candidate = cls._generate_candidate(morphemes, suffixes)

            if PhoneticRules.is_pronounceable(candidate):
                candidates.add(candidate)

            attempts += 1

        return sorted(candidates)

    @classmethod
    def _select_morphemes(cls, brand_language: BrandLanguage) -> list[str]:
        selected = []

        for word in brand_language.vocabulary:
            pools = cls.VOCABULARY_TO_MORPHOLOGY.get(word.lower(), [])

            for pool in pools:
                selected.extend(MorphologyLibrary.by_theme(pool))

        if not selected:
            selected = MorphologyLibrary.all()

        return list(dict.fromkeys(selected))

    @classmethod
    def _select_suffixes(cls, brand_language: BrandLanguage) -> list[str]:
        return cls.STYLE_SUFFIXES.get(
            brand_language.style,
            ["a", "ia", "io", "ora", "ium", "is", "on"],
        )

    @staticmethod
    def _generate_candidate(
        morphemes: list[str],
        suffixes: list[str],
    ) -> str:
        pattern = random.choice(["two_part", "vowel_bridge", "suffix"])

        if pattern == "two_part":
            name = random.choice(morphemes) + random.choice(morphemes)

        elif pattern == "vowel_bridge":
            name = (
                random.choice(morphemes)
                + random.choice(["a", "e", "i", "o", "u"])
                + random.choice(morphemes)
            )

        else:
            name = random.choice(morphemes) + random.choice(suffixes)

        return NamingGenerator._format_name(name)

    @staticmethod
    def _format_name(name: str) -> str:
        return name.lower().capitalize()