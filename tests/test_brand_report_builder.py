from project_origin.brand.decision import NamingDecisionService
from project_origin.brand.knowledge_builder import KnowledgeBuilder
from project_origin.brand.markdown_report import MarkdownReportGenerator
from project_origin.brand.models import FounderProfile
from project_origin.brand.naming.candidate import NameCandidate
from project_origin.brand.report_builder import BrandStrategyReportBuilder


def _profile() -> FounderProfile:
    return FounderProfile(
        problem="Small teams cannot turn noisy signals into clear decisions.",
        audience="technical founders",
        vision="Become the trusted decision layer for early companies.",
        principles="clarity, evidence, and founder control",
        differentiation="turns scattered inputs into explainable priorities",
    )


def _candidate(
    name: str,
    total: float,
    strategy: float,
) -> NameCandidate:
    return NameCandidate(
        name=name,
        pronunciation_score=8.8,
        originality_score=8.0,
        strategy_score=strategy,
        memorability_score=8.2,
        total_score=total,
        evaluation_reason="Evaluated through the naming rubric.",
        metadata={"generation_pattern": "semantic_compound"},
    )


def test_report_builder_uses_decision_evidence_for_consultant_sections():
    profile = _profile()
    knowledge = KnowledgeBuilder.build(profile)
    decision = NamingDecisionService.decide(
        profile=profile,
        knowledge=knowledge,
        candidates=[
            _candidate("Signalbase", 8.8, 8.7),
            _candidate("Clearpath", 8.4, 8.1),
            _candidate("Foundry", 8.0, 7.7),
        ],
    )

    report = BrandStrategyReportBuilder.build(
        profile=profile,
        knowledge=knowledge,
        decision=decision,
    )
    markdown = MarkdownReportGenerator.generate(report)

    assert "## Brand Origin Story" in markdown
    assert "## Brand DNA" in markdown
    assert "| Principle | Meaning | How it shows up |" in markdown
    assert "| Value | Strategic Role | Decision Rule |" in markdown
    assert "## Candidate Comparison" in markdown
    assert "## Next Action Plan" in markdown
    assert "Signalbase" in report.final_recommendation
    assert "Clearpath" in report.candidate_comparison
    assert profile.problem in report.brand_origin_story
    assert len(report.brand_dna_items) >= 3
    assert len(report.strategic_value_items) >= 3
