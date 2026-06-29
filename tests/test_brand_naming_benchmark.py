import json

import pytest

from benchmarks.brand_naming import (
    BrandNamingBenchmarkOutput,
    ProjectOriginNamingRunner,
    evaluate_case_aware_naming,
    evaluate_hard_constraints,
    load_cases,
)
from benchmarks.brand_naming.models import BrandNamingBenchmarkCase


def test_checked_in_benchmark_cases_are_valid_and_unique():
    cases = load_cases()

    assert len(cases) == 5
    assert len({case.identifier for case in cases}) == len(cases)
    assert all(case.expected_themes for case in cases)
    assert all(case.required_qualities for case in cases)
    assert all(case.expected_intent_signals for case in cases)
    assert all(case.known_bad_patterns for case in cases)
    assert all(case.evaluation_rubric.explainability for case in cases)


def test_benchmark_case_rejects_missing_fields():
    with pytest.raises(ValueError, match="missing fields"):
        BrandNamingBenchmarkCase.from_dict({"id": "incomplete"})


def test_loader_rejects_duplicate_ids(tmp_path):
    valid_case = {
        "id": "duplicate",
        "profile": {
            "problem": "Problem",
            "audience": "Audience",
            "vision": "Vision",
            "principles": "Principles",
            "differentiation": "Difference"
        },
        "expected_themes": ["trust"],
        "required_qualities": ["clear"],
        "forbidden_terms": [],
        "expected_intent_signals": [
            {
                "kind": "value",
                "concept": "trust",
                "evidence_hint": "Principles"
            }
        ],
        "known_bad_patterns": ["generic"],
        "evaluation_rubric": {
            "strategic_fit": "Fits the strategy.",
            "distinctiveness": "Avoids clichés.",
            "trustworthiness": "Feels credible.",
            "explainability": "Can be justified from evidence."
        }
    }
    path = tmp_path / "duplicates.json"
    path.write_text(
        json.dumps([valid_case, valid_case]),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="ids must be unique"):
        load_cases(path)


def test_hard_constraint_metrics_detect_forbidden_terms():
    case = load_cases()[0]
    output = BrandNamingBenchmarkOutput(
        case_id=case.identifier,
        approach="test",
        candidates=("Cybera", "Verity", "Sentry", "Lumis", "Axiom"),
        selected_name="Verity",
        reasoning="Test output",
    )

    metrics = evaluate_hard_constraints(case, output)

    assert metrics.has_exactly_five_candidates
    assert metrics.forbidden_term_violations == ("Cybera: cyber",)
    assert not metrics.passed


def test_case_aware_metrics_track_quality_risk_and_confidence():
    case = load_cases()[0]
    output = BrandNamingBenchmarkOutput(
        case_id=case.identifier,
        approach="test",
        candidates=("Hackera", "Verity", "Sentry", "Lumis", "Axiom"),
        selected_name="Verity",
        reasoning="Verity communicates evidence and operator control.",
        candidate_evaluations=(
            {
                "name": "Verity",
                "total_score": 8.5,
                "scores": {
                    "pronunciation": 9.0,
                    "originality": 8.0,
                    "strategic_fit": 8.0,
                    "memorability": 8.0,
                },
            },
            {
                "name": "Hackera",
                "total_score": 8.45,
                "scores": {
                    "pronunciation": 9.0,
                    "originality": 7.0,
                    "strategic_fit": 7.5,
                    "memorability": 8.0,
                },
            },
        ),
    )

    metrics = evaluate_case_aware_naming(case, output)

    assert metrics.selected_required_quality_coverage == 1.0
    assert metrics.score_margin == 0.05
    assert metrics.low_confidence_decision
    assert "Hackera: hacker imagery" in metrics.known_bad_pattern_violations
    assert metrics.average_risk_score > 0


def test_case_aware_metrics_flag_missing_required_qualities():
    case = load_cases()[1]
    output = BrandNamingBenchmarkOutput(
        case_id=case.identifier,
        approach="test",
        candidates=("Harshx", "Coldq"),
        selected_name="Harshx",
        reasoning="Harshx is efficient.",
        candidate_evaluations=(
            {
                "name": "Harshx",
                "total_score": 6.2,
                "scores": {
                    "pronunciation": 6.0,
                    "originality": 6.0,
                    "strategic_fit": 6.0,
                    "memorability": 6.0,
                },
            },
        ),
    )

    metrics = evaluate_case_aware_naming(case, output)

    assert metrics.selected_required_quality_coverage < 1.0
    assert metrics.missing_required_qualities
    assert metrics.low_confidence_decision


def test_benchmark_output_requires_selected_candidate():
    with pytest.raises(ValueError, match="selected_name"):
        BrandNamingBenchmarkOutput(
            case_id="case",
            approach="test",
            candidates=("One", "Two"),
            selected_name="Missing",
            reasoning="Invalid output",
        )


def test_benchmark_output_accepts_candidate_evaluation_trace():
    output = BrandNamingBenchmarkOutput(
        case_id="case",
        approach="test",
        candidates=("One", "Two"),
        selected_name="One",
        reasoning="Trace output",
        candidate_evaluations=(
            {
                "name": "One",
                "total_score": 8.0,
                "scores": {"strategic_fit": 8.0},
                "evaluation_breakdown": {
                    "version": "brand_naming_evaluation_v1",
                },
            },
        ),
    )

    assert output.to_dict()["candidate_evaluations"][0]["name"] == "One"


def test_benchmark_output_rejects_unknown_candidate_evaluation():
    with pytest.raises(ValueError, match="candidate_evaluations"):
        BrandNamingBenchmarkOutput(
            case_id="case",
            approach="test",
            candidates=("One", "Two"),
            selected_name="One",
            reasoning="Trace output",
            candidate_evaluations=(
                {
                    "name": "Missing",
                    "total_score": 8.0,
                    "scores": {},
                },
            ),
        )


def test_project_origin_runner_is_reproducible():
    case = load_cases()[0]
    runner = ProjectOriginNamingRunner(seed=11)

    first = runner.run(case)
    second = runner.run(case)

    assert first.candidates == second.candidates
    assert first.selected_name == second.selected_name
    assert len(first.candidates) == 5
    assert len(first.candidate_evaluations) == 5
    assert first.candidate_evaluations[0]["evaluation_breakdown"]
    assert first.estimated_cost_usd == 0.0
    assert '"approach": "project_origin"' in first.to_json()
