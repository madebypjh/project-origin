"""Run the Project Origin Brand benchmark suite and save a JSON report."""

from argparse import ArgumentParser
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from benchmarks.brand_naming import (  # noqa: E402
    BrandBenchmarkSuite,
    IntentBenchmarkSignal,
    evaluate_intent_quality,
    load_cases,
)
from project_origin.llm.factory import LLMFactory  # noqa: E402


def main() -> None:
    parser = ArgumentParser(
        description="Run Brand naming and intent benchmark cases."
    )
    parser.add_argument(
        "--output",
        default="output/brand_benchmark_report.json",
        help="Path to write the JSON report.",
    )
    parser.add_argument(
        "--no-mock-llm",
        action="store_true",
        help=(
            "Disable deterministic mock LLM shadow intent comparison. "
            "Equivalent to --llm-provider none."
        ),
    )
    parser.add_argument(
        "--llm-provider",
        choices=("mock", "openai", "none"),
        default="mock",
        help="LLM provider for shadow intent comparison.",
    )
    parser.add_argument(
        "--reevaluate-report",
        help=(
            "Recalculate metrics for an existing benchmark report without "
            "rerunning providers."
        ),
    )
    args = parser.parse_args()

    if args.reevaluate_report:
        report_data = _reevaluate_report(PROJECT_ROOT / args.reevaluate_report)
        provider_label = "Reevaluated"
    else:
        provider_name = "none" if args.no_mock_llm else args.llm_provider
        suite = _build_suite(provider_name)
        report = suite.run()
        report_data = report.to_dict()
        provider_label = provider_name.title()

    output_path = PROJECT_ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    summary = report_data["summary"]
    print(f"Saved benchmark report: {output_path}")
    print(f"Cases: {summary['case_count']}")
    print(
        "Naming hard-constraint pass rate: "
        f"{summary['naming_hard_constraint_pass_rate']:.0%}"
    )
    print(
        "Active strict/relaxed intent concept coverage: "
        f"{summary['active_intent']['average_strict_concept_coverage']:.0%}"
        " / "
        f"{summary['active_intent']['average_relaxed_concept_coverage']:.0%}"
    )
    if summary["llm_shadow_intent"] is not None:
        print(
            f"{provider_label} LLM strict/relaxed intent concept "
            "coverage: "
            f"{summary['llm_shadow_intent']['average_strict_concept_coverage']:.0%}"
            " / "
            f"{summary['llm_shadow_intent']['average_relaxed_concept_coverage']:.0%}"
        )


def _build_suite(provider_name: str) -> BrandBenchmarkSuite:
    if provider_name == "none":
        return BrandBenchmarkSuite()
    return BrandBenchmarkSuite(llm_provider=LLMFactory.create(provider_name))


def _reevaluate_report(report_path: Path) -> dict:
    data = json.loads(report_path.read_text(encoding="utf-8"))
    cases_by_id = {case.identifier: case for case in load_cases()}

    for case_report in data["cases"]:
        case = cases_by_id[case_report["case_id"]]
        intent_output = case_report["intent_output"]
        active_metrics = evaluate_intent_quality(
            case,
            _signals_from_json(intent_output["active_signals"]),
        )
        case_report["active_intent_metrics"] = _intent_metrics_to_dict(
            active_metrics
        )

        llm_signals = _signals_from_json(
            intent_output.get("llm_candidate_signals", [])
        )
        if llm_signals:
            llm_metrics = evaluate_intent_quality(case, llm_signals)
            case_report["llm_intent_metrics"] = _intent_metrics_to_dict(
                llm_metrics
            )
        else:
            case_report["llm_intent_metrics"] = None

    data["summary"] = _summary_from_case_reports(data["cases"])
    return data


def _signals_from_json(raw_signals: list[dict]) -> tuple[IntentBenchmarkSignal, ...]:
    return tuple(
        IntentBenchmarkSignal(
            kind=signal["kind"],
            concept=signal["concept"],
            weight=signal["weight"],
            confidence=signal["confidence"],
            evidence=tuple(signal["evidence"]),
        )
        for signal in raw_signals
    )


def _intent_metrics_to_dict(metrics) -> dict:
    return {
        "expected_signal_count": metrics.expected_signal_count,
        "signal_count": metrics.signal_count,
        "expected_concept_matches": metrics.expected_concept_matches,
        "relaxed_concept_matches": metrics.relaxed_concept_matches,
        "expected_evidence_matches": metrics.expected_evidence_matches,
        "missing_expected_concepts": metrics.missing_expected_concepts,
        "relaxed_missing_expected_concepts": (
            metrics.relaxed_missing_expected_concepts
        ),
        "unsupported_evidence": metrics.unsupported_evidence,
        "known_bad_pattern_violations": metrics.known_bad_pattern_violations,
        "strict_concept_coverage": metrics.expected_concept_coverage,
        "relaxed_concept_coverage": metrics.relaxed_concept_coverage,
        "evidence_hint_coverage": metrics.evidence_hint_coverage,
        "passed_grounding": metrics.passed_grounding,
    }


def _summary_from_case_reports(case_reports: list[dict]) -> dict:
    active_metrics = [
        case_report["active_intent_metrics"] for case_report in case_reports
    ]
    llm_metrics = [
        case_report["llm_intent_metrics"]
        for case_report in case_reports
        if case_report["llm_intent_metrics"] is not None
    ]
    naming_passes = [
        case_report["naming_metrics"]["passed"] for case_report in case_reports
    ]

    return {
        "case_count": len(case_reports),
        "naming_hard_constraint_pass_rate": _pass_rate(naming_passes),
        "active_intent": _intent_summary(active_metrics),
        "llm_shadow_intent": (
            _intent_summary(llm_metrics) if llm_metrics else None
        ),
    }


def _intent_summary(metrics: list[dict]) -> dict:
    if not metrics:
        return {
            "average_strict_concept_coverage": 0.0,
            "average_relaxed_concept_coverage": 0.0,
            "average_evidence_hint_coverage": 0.0,
            "grounding_pass_rate": 0.0,
            "known_bad_pattern_violation_count": 0,
        }

    return {
        "average_strict_concept_coverage": _average(
            metric["strict_concept_coverage"] for metric in metrics
        ),
        "average_relaxed_concept_coverage": _average(
            metric["relaxed_concept_coverage"] for metric in metrics
        ),
        "average_evidence_hint_coverage": _average(
            metric["evidence_hint_coverage"] for metric in metrics
        ),
        "grounding_pass_rate": _pass_rate(
            metric["passed_grounding"] for metric in metrics
        ),
        "known_bad_pattern_violation_count": sum(
            len(metric["known_bad_pattern_violations"])
            for metric in metrics
        ),
    }


def _average(values) -> float:
    values = tuple(values)
    if not values:
        return 0.0
    return sum(values) / len(values)


def _pass_rate(values) -> float:
    values = tuple(values)
    if not values:
        return 0.0
    return sum(1 for value in values if value) / len(values)


if __name__ == "__main__":
    main()
