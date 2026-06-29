import pytest

from project_origin.core import (
    IntentNormalizer,
    IntentProfile,
    IntentSignal,
    IntentValidator,
)


def _signal(
    concept: str,
    weight: float,
    evidence: str,
) -> IntentSignal:
    return IntentSignal(
        kind="Value",
        concept=concept,
        weight=weight,
        evidence=(evidence,),
        confidence=0.8,
    )


def test_intent_normalizer_merges_open_ended_concepts():
    normalized = IntentNormalizer.normalize(
        [
            _signal("Medical Humility", 0.4, "medical humility"),
            _signal("medical-humility", 0.6, "replace clinicians"),
        ]
    )

    assert len(normalized) == 1
    assert normalized[0].kind == "value"
    assert normalized[0].concept == "medical_humility"
    assert normalized[0].weight == 1.0
    assert normalized[0].evidence == (
        "medical humility",
        "replace clinicians",
    )


def test_intent_validator_accepts_grounded_evidence():
    signal = _signal("privacy", 1.0, "Privacy comes first")
    profile = IntentProfile(
        domain="brand",
        objective="Build trust",
        signals=(signal,),
    )

    assert (
        IntentValidator.validate(profile, "Privacy comes first for users")
        is profile
    )


def test_intent_validator_rejects_unsupported_evidence():
    signal = _signal("privacy", 1.0, "Invented evidence")
    profile = IntentProfile(
        domain="brand",
        objective="Build trust",
        signals=(signal,),
    )

    with pytest.raises(ValueError, match="not present"):
        IntentValidator.validate(profile, "Only source evidence is valid")


def test_intent_signal_rejects_invalid_probability():
    with pytest.raises(ValueError, match="confidence"):
        IntentSignal(
            kind="value",
            concept="trust",
            weight=1.0,
            evidence=("trust",),
            confidence=1.1,
        )
