import pytest

from project_origin.core import (
    DecisionOption,
    DecisionResult,
    IntentProfile,
    IntentSignal,
    KnowledgeItem,
    KnowledgePacket,
    ReasoningStep,
    ReasoningTrace,
)


def test_core_contracts_capture_an_explainable_decision():
    intent = IntentProfile(
        domain="brand",
        objective="Select a brand direction",
        signals=(
            IntentSignal(
                kind="value",
                concept="trust",
                weight=1.0,
                evidence=("trust",),
                confidence=0.8,
            ),
        ),
    )
    knowledge = KnowledgePacket(
        domain="brand",
        items=(KnowledgeItem(content="Trust is a priority", source="interview"),),
    )
    trace = ReasoningTrace(
        steps=(
            ReasoningStep(
                claim="Option A best reflects trust",
                rationale="It scored highest on the stated priority",
                evidence=("interview",),
                confidence=0.8,
            ),
        ),
    )
    option = DecisionOption(identifier="a", label="Option A")
    result = DecisionResult(
        selected_option_id="a",
        options=(option,),
        rationale="Best strategic fit",
        trace=trace,
        confidence=0.8,
    )

    assert intent.domain == knowledge.domain
    assert result.selected_option_id == option.identifier


def test_decision_result_rejects_unknown_selected_option():
    with pytest.raises(ValueError, match="selected_option_id"):
        DecisionResult(
            selected_option_id="missing",
            options=(DecisionOption(identifier="a", label="Option A"),),
            rationale="Invalid selection",
            trace=ReasoningTrace(steps=()),
        )


def test_decision_result_rejects_duplicate_option_identifiers():
    duplicate = DecisionOption(identifier="same", label="Same")

    with pytest.raises(ValueError, match="identifiers must be unique"):
        DecisionResult(
            selected_option_id="same",
            options=(duplicate, duplicate),
            rationale="Ambiguous",
            trace=ReasoningTrace(steps=()),
        )


def test_core_confidence_must_be_normalized():
    with pytest.raises(ValueError, match="confidence"):
        KnowledgeItem(content="Unsupported", source="test", confidence=1.1)
