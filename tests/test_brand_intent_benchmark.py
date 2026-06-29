from benchmarks.brand_naming import (
    IntentBenchmarkSignal,
    ProjectOriginIntentRunner,
    evaluate_intent_quality,
    load_cases,
)
from project_origin.brand.intent import LlmBrandIntentInterpreter
from project_origin.llm.mock_provider import MockProvider


def test_intent_quality_metrics_track_expected_concepts_and_grounding():
    case = load_cases()[0]
    signals = (
        IntentBenchmarkSignal(
            kind="positioning",
            concept="trusted_decision_layer",
            weight=0.5,
            confidence=0.9,
            evidence=("trusted decision layer",),
        ),
        IntentBenchmarkSignal(
            kind="value",
            concept="operator_control",
            weight=0.5,
            confidence=0.9,
            evidence=("operator control",),
        ),
    )

    metrics = evaluate_intent_quality(case, signals)

    assert metrics.signal_count == 2
    assert metrics.expected_concept_coverage == 2 / 3
    assert metrics.evidence_hint_coverage == 2 / 3
    assert metrics.missing_expected_concepts == (
        "explainable_prioritization",
    )
    assert metrics.passed_grounding


def test_intent_quality_metrics_detect_unsupported_evidence():
    case = load_cases()[0]
    signals = (
        IntentBenchmarkSignal(
            kind="positioning",
            concept="trusted_decision_layer",
            weight=1.0,
            confidence=0.9,
            evidence=("unmentioned magical guarantee",),
        ),
    )

    metrics = evaluate_intent_quality(case, signals)

    assert metrics.unsupported_evidence == (
        "trusted_decision_layer: unmentioned magical guarantee",
    )
    assert not metrics.passed_grounding


def test_project_origin_intent_runner_returns_active_baseline():
    case = load_cases()[0]

    output = ProjectOriginIntentRunner().run(case)

    assert output.case_id == case.identifier
    assert output.approach == "project_origin_intent_shadow"
    assert output.active_signals
    assert output.llm_candidate_signals == ()
    assert output.estimated_cost_usd == 0.0


def test_project_origin_intent_runner_can_include_mock_llm_shadow():
    case = load_cases()[0]

    output = ProjectOriginIntentRunner(
        llm=LlmBrandIntentInterpreter(MockProvider()),
    ).run(case)
    metrics = evaluate_intent_quality(case, output.llm_candidate_signals)

    assert output.llm_error is None
    assert len(output.llm_candidate_signals) == 4
    assert metrics.evidence_hint_coverage >= 2 / 3
    assert metrics.passed_grounding
