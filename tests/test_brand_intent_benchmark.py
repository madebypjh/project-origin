from benchmarks.brand_naming import (
    BrandBenchmarkSuite,
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
    assert metrics.relaxed_concept_coverage == 2 / 3
    assert metrics.evidence_hint_coverage == 2 / 3
    assert metrics.missing_expected_concepts == (
        "explainable_prioritization",
    )
    assert metrics.relaxed_missing_expected_concepts == (
        "explainable_prioritization",
    )
    assert metrics.passed_grounding


def test_intent_quality_metrics_count_relaxed_concept_matches():
    case = load_cases()[0]
    signals = (
        IntentBenchmarkSignal(
            kind="objective",
            concept="become_trusted_decision_layer_for_security_operations",
            weight=0.34,
            confidence=0.9,
            evidence=("trusted decision layer",),
        ),
        IntentBenchmarkSignal(
            kind="value",
            concept="accuracy_evidence_and_operator_control",
            weight=0.33,
            confidence=0.9,
            evidence=("operator control",),
        ),
        IntentBenchmarkSignal(
            kind="differentiation",
            concept="convert_fragmented_findings_into_explainable_priorities",
            weight=0.33,
            confidence=0.9,
            evidence=("explainable priorities",),
        ),
    )

    metrics = evaluate_intent_quality(case, signals)

    assert metrics.expected_concept_coverage == 0.0
    assert metrics.relaxed_concept_coverage == 1.0
    assert metrics.relaxed_missing_expected_concepts == ()


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
    assert len(output.llm_candidate_signals) == 3
    assert metrics.expected_concept_coverage == 1.0
    assert metrics.evidence_hint_coverage == 1.0
    assert metrics.passed_grounding


def test_mock_llm_shadow_covers_all_checked_in_expected_intents():
    runner = ProjectOriginIntentRunner(
        llm=LlmBrandIntentInterpreter(MockProvider()),
    )

    for case in load_cases():
        output = runner.run(case)
        metrics = evaluate_intent_quality(case, output.llm_candidate_signals)

        assert output.llm_error is None
        assert metrics.expected_concept_coverage == 1.0, case.identifier
        assert metrics.evidence_hint_coverage == 1.0, case.identifier
        assert metrics.passed_grounding, case.identifier


def test_brand_benchmark_suite_summarizes_naming_and_intent_results():
    cases = load_cases()[:2]

    report = BrandBenchmarkSuite.with_mock_llm().run(cases)
    summary = report.summary()
    report_dict = report.to_dict()

    assert len(report.cases) == 2
    assert summary["case_count"] == 2
    assert summary["naming_hard_constraint_pass_rate"] == 1.0
    assert summary["active_naming_diversity"]["candidate_count"] == 10
    assert summary["active_naming_case_fit"][
        "average_selected_required_quality_coverage"
    ] >= 0
    assert "low_confidence_decision_rate" in summary["active_naming_case_fit"]
    assert summary["active_intent"]["grounding_pass_rate"] == 1.0
    assert "average_strict_concept_coverage" in summary["active_intent"]
    assert "average_relaxed_concept_coverage" in summary["active_intent"]
    assert summary["llm_shadow_intent"] is not None
    assert summary["intent_shadow_naming"] is not None
    assert summary["intent_shadow_naming"]["diversity"]["candidate_count"] == 10
    assert "case_fit" in summary["intent_shadow_naming"]
    assert "naming_case_metrics" in report_dict["cases"][0]
    assert report_dict["cases"][0]["llm_intent_metrics"] is not None
    assert report_dict["cases"][0]["intent_shadow_naming_output"] is not None
    assert (
        report_dict["cases"][0]["intent_shadow_naming_output"]["approach"]
        == "project_origin_intent_shadow_naming"
    )
