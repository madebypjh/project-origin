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
        "adaptation": ("resilience", "planning", "asset"),
        "asset": ("resilience", "planning", "trace"),
        "audience": ("focus", "identity"),
        "clarity": ("clarity", "focus", "direction"),
        "clause": ("clause", "review", "caution"),
        "climate": ("resilience", "scenario", "asset"),
        "clinician": ("trust", "care"),
        "consent": ("privacy", "control", "agency"),
        "control": ("alignment", "focus", "confidence"),
        "contract": ("clause", "review", "caution"),
        "creative": ("voice", "story", "identity"),
        "creator": ("identity", "voice", "originality"),
        "decision": ("decision", "logic", "framework"),
        "evidence": ("proof", "truth", "integrity"),
        "explainable": ("clarity", "proof", "logic"),
        "family": ("care", "privacy", "safety"),
        "fleet": ("fleet", "operator", "signal"),
        "finance": ("clarity", "direction", "framework"),
        "founder": ("clarity", "direction", "framework"),
        "guidance": ("direction", "clarity"),
        "habit": ("care", "rhythm", "balance"),
        "health": ("care", "clarity", "trust"),
        "humility": ("integrity", "trust", "care"),
        "industrial": ("precision", "system", "integrity"),
        "learner": ("learn", "guide", "progress"),
        "learning": ("learn", "guide", "progress"),
        "legal": ("clause", "review", "caution"),
        "logistics": ("route", "flow", "visibility"),
        "manufacturing": ("system", "origin", "precision"),
        "material": ("origin", "proof", "system"),
        "municipal": ("resilience", "asset", "planning"),
        "operator": ("control", "focus", "alignment"),
        "ownership": ("identity", "integrity"),
        "priority": ("focus", "decision", "signal"),
        "provenance": ("origin", "proof", "trace"),
        "recycled": ("origin", "cycle", "proof"),
        "responsible": ("integrity", "trust"),
        "robot": ("fleet", "operator", "safety"),
        "robotic": ("fleet", "operator", "safety"),
        "route": ("route", "flow", "visibility"),
        "runway": ("clarity", "path", "direction"),
        "security": ("proof", "signal", "control"),
        "shipment": ("route", "flow", "visibility"),
        "student": ("learn", "guide", "progress"),
        "story": ("story", "voice", "identity"),
        "stress": ("calm", "reflect", "support"),
        "traceability": ("proof", "origin", "integrity"),
        "trusted": ("truth", "integrity", "confidence"),
        "verified": ("proof", "integrity", "origin"),
        "vulnerability": ("signal", "priority", "control"),
        "voice": ("voice", "story", "identity"),
    }

    @classmethod
    def build(cls, intent: IntentProfile) -> BrandLanguage:
        concepts = [signal.concept for signal in intent.signals]
        evidence = [
            evidence_item
            for signal in intent.signals
            for evidence_item in signal.evidence
        ]
        tokens = cls._tokens([*concepts, *evidence])
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
        if token_set & {"student", "learner", "learning", "education"}:
            return "encouraging", "confidence", "clear"
        if token_set & {"health", "medical", "empathy", "humility", "care"}:
            return "humane", "trust", "clear"
        if token_set & {"stress", "therapy", "wellbeing", "reflective"}:
            return "gentle", "calm", "clear"
        if token_set & {"legal", "contract", "clause", "attorney"}:
            return "cautious", "trust", "structured"
        if token_set & {"privacy", "consent", "profiled", "watched"}:
            return "respectful", "safety", "clear"
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
            "logistics",
            "shipment",
            "warehouse",
            "robot",
            "robotic",
            "fleet",
        }:
            return "credible", "confidence", "structured"
        if token_set & {"climate", "resilience", "municipal", "asset"}:
            return "evidence-led", "clarity", "structured"
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
            "contracts": "contract",
            "creators": "creator",
            "families": "family",
            "founders": "founder",
            "habits": "habit",
            "learners": "learner",
            "manufacturers": "manufacturing",
            "materials": "material",
            "parents": "parent",
            "priorities": "priority",
            "prioritization": "priority",
            "prioritisation": "priority",
            "robots": "robot",
            "signals": "signal",
            "shipments": "shipment",
            "students": "student",
            "stories": "story",
            "vulnerabilities": "vulnerability",
        }
        return variants.get(token, token)
