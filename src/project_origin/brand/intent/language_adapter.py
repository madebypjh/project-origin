"""Build BrandLanguage from evidence-backed intent signals."""

import re

from project_origin.brand.models import BrandLanguage
from project_origin.core import IntentProfile


class BrandLanguageFromIntent:
    STOPWORDS = {
        "and",
        "at",
        "for",
        "from",
        "in",
        "into",
        "of",
        "the",
        "to",
        "with",
    }

    BRIDGE_VOCABULARY = {
        "accuracy": ("precision", "proof", "clarity"),
        "audience": ("focus", "identity"),
        "clarity": ("clarity", "focus", "direction"),
        "clinician": ("trust", "care"),
        "control": ("alignment", "focus", "confidence"),
        "creator": ("identity", "voice", "originality"),
        "decision": ("decision", "logic", "framework"),
        "evidence": ("proof", "truth", "integrity"),
        "finance": ("clarity", "direction", "framework"),
        "guidance": ("direction", "clarity"),
        "health": ("care", "clarity", "trust"),
        "humility": ("integrity", "trust", "care"),
        "industrial": ("precision", "system", "integrity"),
        "material": ("origin", "proof", "system"),
        "operator": ("control", "focus", "alignment"),
        "ownership": ("identity", "integrity"),
        "priority": ("focus", "decision", "signal"),
        "provenance": ("origin", "proof", "trace"),
        "responsible": ("integrity", "trust"),
        "traceability": ("proof", "origin", "integrity"),
        "trusted": ("truth", "integrity", "confidence"),
        "voice": ("voice", "story", "identity"),
    }

    @classmethod
    def build(cls, intent: IntentProfile) -> BrandLanguage:
        concepts = [signal.concept for signal in intent.signals]
        tokens = cls._tokens(concepts)
        vocabulary = cls._vocabulary(tokens)
        tone, emotion, style = cls._language_attributes(tokens)
        direction = cls._semantic_direction(concepts, tone, emotion, style)

        return BrandLanguage(
            vocabulary=vocabulary,
            tone=tone,
            emotion=emotion,
            style=style,
            semantic_direction=direction,
        )

    @classmethod
    def _tokens(cls, concepts: list[str]) -> list[str]:
        tokens = []
        for concept in concepts:
            for token in re.split(r"[^a-z0-9]+", concept.casefold()):
                if token and token not in cls.STOPWORDS:
                    tokens.append(cls._normalize_token(token))
        return list(dict.fromkeys(tokens))

    @classmethod
    def _vocabulary(cls, tokens: list[str]) -> list[str]:
        vocabulary = list(tokens)
        for token in tokens:
            vocabulary.extend(cls.BRIDGE_VOCABULARY.get(token, ()))

        if not vocabulary:
            vocabulary = ["clarity", "direction", "identity", "trust"]

        return list(dict.fromkeys(vocabulary))

    @classmethod
    def _language_attributes(
        cls,
        tokens: list[str],
    ) -> tuple[str, str, str]:
        token_set = set(tokens)

        if token_set & {"creator", "voice", "originality", "story"}:
            return "imaginative", "inspiration", "expressive"
        if token_set & {"health", "medical", "empathy", "humility", "care"}:
            return "humane", "trust", "clear"
        if token_set & {
            "finance",
            "runway",
            "responsible",
            "decision",
            "priority",
        }:
            return "strategic", "clarity", "structured"
        if token_set & {
            "industrial",
            "material",
            "provenance",
            "traceability",
            "procurement",
        }:
            return "credible", "confidence", "structured"
        if token_set & {"trusted", "evidence", "operator", "control"}:
            return "credible", "trust", "structured"

        return "balanced", "confidence", "clear"

    @staticmethod
    def _semantic_direction(
        concepts: list[str],
        tone: str,
        emotion: str,
        style: str,
    ) -> str:
        if concepts:
            top_concepts = ", ".join(concepts[:5])
        else:
            top_concepts = "the founder's stated intent"

        return (
            "The brand language should reflect interpreted intent signals: "
            f"{top_concepts}. Use a {tone} tone, {emotion} emotion, and "
            f"{style} style."
        )

    @staticmethod
    def _normalize_token(token: str) -> str:
        variants = {
            "priorities": "priority",
            "prioritization": "priority",
            "prioritisation": "priority",
        }
        return variants.get(token, token)
