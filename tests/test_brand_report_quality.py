from project_origin.brand.decision import NamingDecisionService
from project_origin.brand.application import BrandApplication
from project_origin.brand.knowledge_builder import KnowledgeBuilder
from project_origin.brand.models import (
    BrandStrategyReport,
    FounderProfile,
    NameRecommendation,
)
from project_origin.brand.naming.candidate import NameCandidate
from project_origin.brand.report_builder import BrandStrategyReportBuilder
from project_origin.brand.report_quality import ReportQualityEvaluator
from project_origin.llm.mock_provider import MockProvider


def _profile() -> FounderProfile:
    return FounderProfile(
        problem="Founders lack a clear way to choose a brand direction.",
        audience="early-stage founders",
        vision="Become the trusted decision layer for brand strategy.",
        principles="clarity, evidence, and founder control",
        differentiation="turns messy founder context into explainable decisions",
    )


def _decision(profile: FounderProfile):
    knowledge = KnowledgeBuilder.build(profile)
    candidates = [
        NameCandidate(
            name="Signalbase",
            pronunciation_score=8.8,
            originality_score=8.2,
            strategy_score=8.8,
            memorability_score=8.4,
            total_score=8.9,
            evaluation_reason="Evaluated through the naming rubric.",
            metadata={"generation_pattern": "semantic_compound"},
        ),
        NameCandidate(
            name="Clearpath",
            pronunciation_score=8.5,
            originality_score=8.0,
            strategy_score=8.1,
            memorability_score=8.2,
            total_score=8.4,
            evaluation_reason="Evaluated through the naming rubric.",
            metadata={"generation_pattern": "semantic_compound"},
        ),
        NameCandidate(
            name="Originlab",
            pronunciation_score=8.1,
            originality_score=7.8,
            strategy_score=7.7,
            memorability_score=8.0,
            total_score=8.0,
            evaluation_reason="Evaluated through the naming rubric.",
            metadata={"generation_pattern": "suffix"},
        ),
        NameCandidate(
            name="Trustaxis",
            pronunciation_score=8.0,
            originality_score=7.6,
            strategy_score=7.5,
            memorability_score=7.9,
            total_score=7.8,
            evaluation_reason="Evaluated through the naming rubric.",
            metadata={"generation_pattern": "compressed_compound"},
        ),
        NameCandidate(
            name="Foundry",
            pronunciation_score=8.0,
            originality_score=7.4,
            strategy_score=7.2,
            memorability_score=7.8,
            total_score=7.6,
            evaluation_reason="Evaluated through the naming rubric.",
            metadata={"generation_pattern": "short_root"},
        ),
    ]
    return knowledge, NamingDecisionService.decide(profile, knowledge, candidates)


def test_report_quality_evaluator_passes_structured_builder_report():
    profile = _profile()
    knowledge, decision = _decision(profile)
    report = BrandStrategyReportBuilder.build(profile, knowledge, decision)

    result = ReportQualityEvaluator.evaluate(report, profile, decision)

    assert result.passed
    assert result.total_score >= 22
    assert not result.automatic_failures
    assert not result.missing_sections


def test_report_quality_evaluator_fails_generic_incomplete_report():
    profile = _profile()
    recommendation = NameRecommendation(
        name="Generic",
        meaning="Name",
        strategic_fit="Okay",
        strengths="Nice",
        weaknesses="None",
        score=8.0,
        score_reason="Good",
    )
    report = BrandStrategyReport(
        executive_summary="A great innovative solution.",
        founder_insights="The founder wants a brand.",
        brand_identity="A brand.",
        mission_statement="Make brands.",
        vision_statement="Grow.",
        core_values="Trust",
        positioning="Good brand",
        target_audience="Founders",
        brand_personality="Sage",
        naming_strategy="Pick a good name.",
        name_recommendations=[recommendation],
        final_recommendation="Generic is good.",
    )

    result = ReportQualityEvaluator.evaluate(report, profile)

    assert not result.passed
    assert "report must include exactly five name candidates" in (
        result.automatic_failures
    )
    assert result.missing_sections


def test_application_report_quality_gate_accepts_builder_report():
    profile = _profile()
    knowledge, decision = _decision(profile)
    report = BrandStrategyReportBuilder.build(profile, knowledge, decision)
    app = BrandApplication(provider=MockProvider())

    app._evaluate_report_quality(report, profile, decision)
