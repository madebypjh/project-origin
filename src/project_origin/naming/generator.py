"""
Project Origin - Semantic Naming Generator

Generates original brand name candidates from SemanticProfile.
"""

import random

from src.project_origin.models import SemanticProfile
from src.project_origin.naming.morphology import MorphologyLibrary
from src.project_origin.naming.phonetics import PhoneticRules


class NamingGenerator:
    DEFAULT_CANDIDATE_COUNT = 100

    THEME_TO_MORPHOLOGY = {
        "technology": ["tech", "greek", "strategy"],
        "trust": ["trust", "latin", "strategy"],
        "strategy": ["strategy", "latin", "tech"],
        "premium": ["premium", "latin"],
        "discovery": ["latin", "greek", "tech"],
        "creativity": ["premium", "greek", "latin"],
    }

    @classmethod
    def generate(
        cls,
        semantic_profile: SemanticProfile,
        count: int = DEFAULT_CANDIDATE_COUNT,
    ) -> list[str]:
        morphemes = cls._select_morphemes(semantic_profile)
        candidates = set()

        attempts = 0
        max_attempts = count * 20

        while len(candidates) < count and attempts < max_attempts:
            candidate = cls._generate_candidate(morphemes)

            if PhoneticRules.is_pronounceable(candidate):
                candidates.add(candidate)

            attempts += 1

        return sorted(candidates)

    @classmethod
    def _select_morphemes(cls, semantic_profile: SemanticProfile) -> list[str]:
        selected = []

        for theme in semantic_profile.themes:
            pools = cls.THEME_TO_MORPHOLOGY.get(theme, [])

            for pool in pools:
                selected.extend(MorphologyLibrary.by_theme(pool))

        if not selected:
            selected = MorphologyLibrary.all()

        return list(dict.fromkeys(selected))

    @staticmethod
    def _generate_candidate(morphemes: list[str]) -> str:
        pattern = random.choice(["two_part", "three_part", "suffix"])

        if pattern == "two_part":
            first = random.choice(morphemes)
            second = random.choice(morphemes)
            name = first + second

        elif pattern == "three_part":
            first = random.choice(morphemes)
            middle = random.choice(["a", "e", "i", "o", "u"])
            second = random.choice(morphemes)
            name = first + middle + second

        else:
            first = random.choice(morphemes)
            suffix = random.choice(["a", "ia", "io", "ora", "ium", "is", "on"])
            name = first + suffix

        return NamingGenerator._format_name(name)

    @staticmethod
    def _format_name(name: str) -> str:
        return name.lower().capitalize()