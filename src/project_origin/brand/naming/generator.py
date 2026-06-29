"""
Project Origin - Semantic Naming Generator

Generates original brand name candidates from BrandLanguage.
"""

import random

from project_origin.brand.models import BrandLanguage
from project_origin.brand.naming.candidate import NameCandidate
from project_origin.brand.naming.morphology import MorphologyLibrary
from project_origin.brand.naming.phonetics import PhoneticRules


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
        "proof": ["trust", "discovery"],
        "trace": ["discovery", "industrial"],
        "identity": ["creativity", "premium"],
        "story": ["creativity"],
        "voice": ["creativity"],
        "originality": ["creativity"],
        "care": ["care", "trust"],
        "rhythm": ["care"],
        "balance": ["care", "premium"],
        "cycle": ["discovery", "industrial"],
        "material": ["industrial", "discovery"],
        "source": ["industrial", "discovery"],
        "learn": ["education", "care"],
        "guide": ["education", "strategy"],
        "step": ["education", "strategy"],
        "growth": ["education", "creativity"],
        "progress": ["education", "strategy"],
        "student": ["education", "care"],
        "learner": ["education", "care"],
        "clause": ["legal", "trust"],
        "review": ["legal", "strategy"],
        "caution": ["legal", "trust"],
        "boundary": ["legal", "wellness"],
        "risk": ["legal", "climate", "strategy"],
        "contract": ["legal", "trust"],
        "resilience": ["climate", "industrial"],
        "scenario": ["climate", "strategy"],
        "asset": ["climate", "industrial"],
        "adapt": ["climate", "discovery"],
        "planning": ["climate", "strategy"],
        "privacy": ["privacy", "trust"],
        "consent": ["privacy", "trust"],
        "control": ["privacy", "robotics", "strategy"],
        "local": ["privacy"],
        "personal": ["privacy", "care"],
        "route": ["logistics", "strategy"],
        "flow": ["logistics", "industrial"],
        "shipment": ["logistics", "industrial"],
        "visibility": ["logistics", "discovery"],
        "escalation": ["logistics", "strategy"],
        "robot": ["robotics", "industrial"],
        "fleet": ["robotics", "logistics"],
        "operator": ["robotics", "strategy"],
        "safety": ["robotics", "trust"],
        "warehouse": ["robotics", "logistics"],
        "calm": ["wellness", "care"],
        "reflect": ["wellness", "creativity"],
        "gentle": ["wellness", "care"],
        "support": ["wellness", "care"],
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
        seed: int | None = None,
    ) -> list[NameCandidate]:
        if count < 0:
            raise ValueError("count must be non-negative")

        morphemes = cls._select_morphemes(brand_language)
        suffixes = cls._select_suffixes(brand_language)
        random_source = random.Random(seed)

        candidates = set()
        attempts = 0
        max_attempts = count * 30

        while len(candidates) < count and attempts < max_attempts:
            candidate = cls._generate_candidate(
                morphemes,
                suffixes,
                random_source,
            )

            if PhoneticRules.is_pronounceable(candidate):
                candidates.add(candidate)

            attempts += 1

        return [
            NameCandidate(
                name=name,
                style=brand_language.style,
                metadata={"semantic_direction": brand_language.semantic_direction},
            )
            for name in sorted(candidates)
        ]

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
        random_source: random.Random,
    ) -> str:
        pattern = random_source.choice(["two_part", "vowel_bridge", "suffix"])

        if pattern == "two_part":
            name = random_source.choice(morphemes) + random_source.choice(morphemes)

        elif pattern == "vowel_bridge":
            name = (
                random_source.choice(morphemes)
                + random_source.choice(["a", "e", "i", "o", "u"])
                + random_source.choice(morphemes)
            )

        else:
            name = random_source.choice(morphemes) + random_source.choice(suffixes)

        return NamingGenerator._format_name(name)

    @staticmethod
    def _format_name(name: str) -> str:
        return name.lower().capitalize()
