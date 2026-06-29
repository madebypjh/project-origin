"""
Project Origin - Semantic Engine

Orchestrates theme detection and vocabulary building.
"""

from project_origin.brand.models import FounderProfile, SemanticProfile
from project_origin.brand.semantic.theme_detector import ThemeDetector
from project_origin.brand.semantic.vocabulary_builder import VocabularyBuilder


class SemanticEngine:
    @classmethod
    def build(cls, profile: FounderProfile) -> SemanticProfile:
        themes = ThemeDetector.detect(profile)
        dominant_theme = cls._get_dominant_theme(themes)
        vocabulary = VocabularyBuilder.build(themes)
        keywords = cls._extract_keywords(profile, vocabulary)

        return SemanticProfile(
            themes=themes,
            keywords=keywords,
            vocabulary=vocabulary,
            dominant_theme=dominant_theme,
        )

    @staticmethod
    def _get_dominant_theme(themes: dict[str, float]) -> str:
        return max(themes, key=themes.get)

    @staticmethod
    def _extract_keywords(
        profile: FounderProfile,
        vocabulary: list[str],
    ) -> list[str]:
        text = " ".join(
            [
                profile.problem,
                profile.audience,
                profile.vision,
                profile.principles,
                profile.differentiation,
            ]
        ).lower()

        found_keywords = [
            word for word in vocabulary
            if word.lower() in text
        ]

        if found_keywords:
            return found_keywords

        return vocabulary[:8]
