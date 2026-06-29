import json

import pytest

from project_origin.brand.decision import NamingDecisionService
from project_origin.brand.knowledge_builder import KnowledgeBuilder
from project_origin.brand.models import FounderProfile
from project_origin.brand.naming.candidate import NameCandidate
from project_origin.brand.report_parser import ReportParser
from project_origin.llm.mock_provider import MockProvider


def _decision():
    profile = FounderProfile(
        problem="Unclear decisions",
        audience="founders",
        vision="Trusted intelligence",
        principles="Truth",
        differentiation="Evidence",
    )
    knowledge = KnowledgeBuilder.build(profile)
    candidates = [
        NameCandidate(
            name=f"Option{i}",
            pronunciation_score=8,
            originality_score=8,
            strategy_score=9 if i == 0 else 7,
            memorability_score=8,
            total_score=9 - i * 0.2,
            evaluation_reason="Evaluated",
        )
        for i in range(5)
    ]
    return NamingDecisionService.decide(profile, knowledge, candidates).result


def test_mock_report_preserves_decision():
    decision = _decision()
    selected = decision.options[0].label
    prompt = (
        f"Selected name: {selected}\n"
        + "\n".join(
            f"- {option.label}: total={option.scores['total']}/10"
            for option in decision.options
        )
    )

    report = ReportParser.parse(MockProvider().generate(prompt), decision)

    assert report.name_recommendations[0].name == selected
    assert selected in report.final_recommendation


def test_parser_rejects_name_outside_decision():
    decision = _decision()
    raw = json.loads(MockProvider().generate("ignored"))

    with pytest.raises(ValueError, match="outside the DecisionResult"):
        ReportParser.parse(json.dumps(raw), decision)
