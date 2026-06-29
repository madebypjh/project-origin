"""Deterministic fallback and baseline for Brand intent interpretation."""

from project_origin.brand.intent.adapter import BrandIntentAdapter
from project_origin.brand.models import FounderProfile
from project_origin.brand.semantic.theme_detector import ThemeDetector
from project_origin.core import (
    IntentNormalizer,
    IntentProfile,
    IntentSignal,
    IntentValidator,
)


class RuleBasedBrandIntentInterpreter:
    def interpret(self, input_data: FounderProfile) -> IntentProfile:
        matches = ThemeDetector.matched_keywords(input_data)
        detected_themes = ThemeDetector.detect(input_data)

        raw_signals = []
        for theme, evidence in matches.items():
            if not evidence or theme not in detected_themes:
                continue
            raw_signals.append(
                IntentSignal(
                    kind="semantic_theme",
                    concept=theme,
                    weight=detected_themes[theme],
                    evidence=evidence,
                    confidence=0.65,
                    metadata={"source": "rule_based"},
                )
            )

        signals = IntentNormalizer.normalize(raw_signals)
        unresolved = ()
        if not signals:
            unresolved = (
                "No evidence-backed semantic theme was detected by rules.",
            )

        profile = BrandIntentAdapter.to_intent_profile(
            input_data,
            signals=signals,
            unresolved_signals=unresolved,
        )
        return IntentValidator.validate(
            profile,
            BrandIntentAdapter.source_text(input_data),
        )
