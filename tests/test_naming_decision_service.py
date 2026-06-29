import pytest

from project_origin.brand.decision import NamingDecisionService
from project_origin.brand.knowledge_builder import KnowledgeBuilder
from project_origin.brand.models import FounderProfile
from project_origin.brand.naming.candidate import NameCandidate


def _profile() -> FounderProfile:
    return FounderProfile(
        problem="Founders cannot explain complex strategic decisions",
        audience="early-stage founders",
        vision="Become a trusted decision intelligence platform",
        principles="Truth and explainability",
        differentiation="Structured evidence-backed reasoning",
    )


def _candidate(
    name: str,
    total: float,
    strategy: float,
    originality: float = 8.0,
) -> NameCandidate:
    return NameCandidate(
        name=name,
        pronunciation_score=8.0,
        originality_score=originality,
        strategy_score=strategy,
        memorability_score=8.0,
        total_score=total,
        evaluation_reason=f"{name} was evaluated by the naming rubric.",
    )


def test_service_returns_complete_core_decision_record():
    profile = _profile()
    knowledge = KnowledgeBuilder.build(profile)

    record = NamingDecisionService.decide(
        profile,
        knowledge,
        [
            _candidate("Veriora", 8.7, 9.0),
            _candidate("Nexora", 8.2, 8.0),
        ],
    )

    assert record.intent.domain == "brand"
    assert record.knowledge.domain == "brand"
    assert record.result.selected_option_id == "veriora"
    assert record.result.options[0].label == "Veriora"
    assert record.result.trace.steps
    assert record.result.warnings
    assert '"selected_option_id": "veriora"' in record.to_json()


def test_service_uses_deterministic_tie_breaking():
    profile = _profile()
    knowledge = KnowledgeBuilder.build(profile)

    record = NamingDecisionService.decide(
        profile,
        knowledge,
        [
            _candidate("Zeta", 8.0, 8.0),
            _candidate("Alpha", 8.0, 8.0),
        ],
    )

    assert record.result.selected_option_id == "alpha"


def test_service_rejects_unevaluated_candidates():
    profile = _profile()
    knowledge = KnowledgeBuilder.build(profile)

    with pytest.raises(ValueError, match="evaluated"):
        NamingDecisionService.decide(
            profile,
            knowledge,
            [NameCandidate(name="NoScore")],
        )
