"""
Project Origin - Brand Language Engine

Transforms SemanticProfile into BrandLanguage.
"""

from project_origin.brand.models import BrandLanguage, SemanticProfile


class BrandLanguageEngine:
    TONE_BY_THEME = {
        "technology": "analytical",
        "trust": "credible",
        "strategy": "strategic",
        "premium": "refined",
        "discovery": "exploratory",
        "creativity": "imaginative",
        "care": "humane",
        "industrial": "grounded",
    }

    EMOTION_BY_THEME = {
        "technology": "confidence",
        "trust": "trust",
        "strategy": "clarity",
        "premium": "aspiration",
        "discovery": "curiosity",
        "creativity": "inspiration",
        "care": "calm",
        "industrial": "confidence",
    }

    STYLE_BY_THEME = {
        "technology": "modern",
        "trust": "clear",
        "strategy": "structured",
        "premium": "minimal",
        "discovery": "open",
        "creativity": "expressive",
        "care": "clear",
        "industrial": "structured",
    }

    @classmethod
    def build(cls, semantic_profile: SemanticProfile) -> BrandLanguage:
        dominant_theme = semantic_profile.dominant_theme

        tone = cls.TONE_BY_THEME.get(dominant_theme, "balanced")
        emotion = cls.EMOTION_BY_THEME.get(dominant_theme, "confidence")
        style = cls.STYLE_BY_THEME.get(dominant_theme, "clear")

        vocabulary = cls._expand_vocabulary(semantic_profile)

        semantic_direction = cls._build_semantic_direction(
            dominant_theme=dominant_theme,
            tone=tone,
            emotion=emotion,
            style=style,
        )

        return BrandLanguage(
            vocabulary=vocabulary,
            tone=tone,
            emotion=emotion,
            style=style,
            semantic_direction=semantic_direction,
        )

    @staticmethod
    def _expand_vocabulary(semantic_profile: SemanticProfile) -> list[str]:
        vocabulary = list(semantic_profile.vocabulary)

        expansion_words = {
            "technology": [
                "reasoning",
                "intelligence",
                "system",
                "logic",
                "signal",
            ],
            "trust": [
                "truth",
                "clarity",
                "integrity",
                "confidence",
                "proof",
            ],
            "strategy": [
                "direction",
                "alignment",
                "decision",
                "framework",
                "focus",
            ],
            "premium": [
                "quality",
                "precision",
                "elegance",
                "refinement",
                "excellence",
            ],
            "discovery": [
                "insight",
                "origin",
                "path",
                "reveal",
                "exploration",
            ],
            "creativity": [
                "identity",
                "voice",
                "story",
                "imagination",
                "originality",
            ],
            "care": [
                "care",
                "balance",
                "rhythm",
                "clarity",
                "trust",
            ],
            "industrial": [
                "material",
                "source",
                "origin",
                "proof",
                "system",
                "precision",
            ],
        }

        for theme in semantic_profile.themes:
            vocabulary.extend(expansion_words.get(theme, []))

        return list(dict.fromkeys(vocabulary))

    @staticmethod
    def _build_semantic_direction(
        dominant_theme: str,
        tone: str,
        emotion: str,
        style: str,
    ) -> str:
        return (
            f"The brand language should emphasize {dominant_theme}, "
            f"with a {tone} tone, {emotion} emotion, and {style} style."
        )
