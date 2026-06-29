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
    CONTROLLED_LITERAL_THEMES = ("intuitive", "literal_tech")
    LITERAL_TECH_SIGNALS = {
        "ai",
        "agent",
        "automation",
        "cloud",
        "code",
        "data",
        "developer",
        "engine",
        "infrastructure",
        "intelligence",
        "model",
        "platform",
        "research",
        "software",
        "system",
        "workflow",
    }
    PATTERN_WEIGHTS = (
        ("semantic_compound", 0.24),
        ("compressed_compound", 0.20),
        ("suffix", 0.18),
        ("vowel_bridge", 0.16),
        ("humanized", 0.14),
        ("short_root", 0.08),
    )

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
        controlled_morphemes = cls._select_controlled_morphemes(brand_language)
        suffixes = cls._select_suffixes(brand_language)
        random_source = random.Random(seed)

        candidates: dict[str, tuple[str, tuple[str, ...]]] = {}
        attempts = 0
        max_attempts = count * 30

        while len(candidates) < count and attempts < max_attempts:
            candidate, pattern, roots = cls._generate_candidate(
                morphemes,
                controlled_morphemes,
                suffixes,
                random_source,
            )

            if PhoneticRules.is_pronounceable(candidate):
                candidates.setdefault(candidate, (pattern, roots))

            attempts += 1

        return [
            NameCandidate(
                name=name,
                style=brand_language.style,
                metadata=cls._candidate_metadata(
                    semantic_direction=brand_language.semantic_direction,
                    pattern=pattern,
                    roots=roots,
                ),
            )
            for name, (pattern, roots) in sorted(candidates.items())
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
    def _select_controlled_morphemes(
        cls,
        brand_language: BrandLanguage,
    ) -> list[str]:
        selected = []
        for theme in cls.CONTROLLED_LITERAL_THEMES:
            selected.extend(MorphologyLibrary.by_theme(theme))

        intent_text = " ".join(
            [
                *brand_language.vocabulary,
                brand_language.semantic_direction,
                brand_language.tone,
                brand_language.emotion,
                brand_language.style,
            ]
        ).casefold()
        literal_signal_count = sum(
            1
            for signal in cls.LITERAL_TECH_SIGNALS
            if signal in intent_text
        )

        if literal_signal_count == 0:
            selected = [
                morpheme
                for morpheme in selected
                if morpheme not in MorphologyLibrary.LITERAL_TECH_SOUNDS
            ]
        elif literal_signal_count >= 2:
            selected.extend(MorphologyLibrary.LITERAL_TECH_SOUNDS)

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
        controlled_morphemes: list[str],
        suffixes: list[str],
        random_source: random.Random,
    ) -> tuple[str, str, tuple[str, ...]]:
        pattern = NamingGenerator._choose_pattern(random_source)
        first = NamingGenerator._choose_morpheme(
            morphemes,
            controlled_morphemes,
            random_source,
        )
        second = NamingGenerator._choose_morpheme(
            morphemes,
            controlled_morphemes,
            random_source,
        )
        roots = (first, second)

        if pattern == "semantic_compound":
            name = first + second

        elif pattern == "vowel_bridge":
            name = (
                first
                + random_source.choice(["a", "e", "i", "o", "u"])
                + second
            )

        elif pattern == "compressed_compound":
            name = NamingGenerator._head(first) + NamingGenerator._head(second)

        elif pattern == "humanized":
            name = NamingGenerator._head(first) + random_source.choice(
                ["ra", "la", "na", "ma", "ara", "ora", "elle"]
            )
            roots = (first,)

        elif pattern == "short_root":
            name = NamingGenerator._head(first) + random_source.choice(
                ["a", "o", "i", "el", "is", "on"]
            )
            roots = (first,)

        else:
            name = first + random_source.choice(suffixes)
            roots = (first,)

        return NamingGenerator._format_name(name), pattern, roots

    @staticmethod
    def _choose_pattern(random_source: random.Random) -> str:
        patterns = [pattern for pattern, _weight in NamingGenerator.PATTERN_WEIGHTS]
        weights = [weight for _pattern, weight in NamingGenerator.PATTERN_WEIGHTS]
        return random_source.choices(patterns, weights=weights, k=1)[0]

    @staticmethod
    def _choose_morpheme(
        core_morphemes: list[str],
        controlled_morphemes: list[str],
        random_source: random.Random,
    ) -> str:
        if controlled_morphemes and random_source.random() < 0.18:
            return random_source.choice(controlled_morphemes)

        return random_source.choice(core_morphemes)

    @staticmethod
    def _head(morpheme: str) -> str:
        if len(morpheme) <= 4:
            return morpheme

        return morpheme[:4]

    @staticmethod
    def _candidate_metadata(
        semantic_direction: str,
        pattern: str,
        roots: tuple[str, ...],
    ) -> dict[str, str | tuple[str, ...]]:
        normalized_roots = tuple(
            NamingGenerator._head(root.casefold()) for root in roots
        )
        signature = ":".join(sorted(normalized_roots))

        return {
            "semantic_direction": semantic_direction,
            "generation_pattern": pattern,
            "generation_roots": normalized_roots,
            "generation_signature": signature,
        }

    @staticmethod
    def _format_name(name: str) -> str:
        return name.lower().capitalize()
