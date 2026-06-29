"""Validate that interpreted intent remains grounded in source input."""

import re

from project_origin.core.intent.models import IntentProfile


class IntentValidator:
    WEIGHT_TOLERANCE = 0.001

    @classmethod
    def validate(
        cls,
        profile: IntentProfile,
        source_text: str,
    ) -> IntentProfile:
        normalized_source = cls._normalize_text(source_text)
        if not normalized_source:
            raise ValueError("Intent source text must not be empty")

        keys = [
            (signal.kind.casefold(), signal.concept.casefold())
            for signal in profile.signals
        ]
        if len(keys) != len(set(keys)):
            raise ValueError("Intent signals must be unique after normalization")

        if profile.signals:
            weight_sum = sum(signal.weight for signal in profile.signals)
            if abs(weight_sum - 1.0) > cls.WEIGHT_TOLERANCE:
                raise ValueError("Intent signal weights must sum to 1.0")

        for signal in profile.signals:
            for evidence in signal.evidence:
                normalized_evidence = cls._normalize_text(evidence)
                if normalized_evidence not in normalized_source:
                    raise ValueError(
                        "Intent evidence is not present in source input: "
                        f"{evidence}"
                    )

        return profile

    @staticmethod
    def _normalize_text(value: str) -> str:
        return re.sub(r"\s+", " ", value).strip().casefold()
