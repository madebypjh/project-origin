"""Run Brand benchmark cases and serialize comparable reports."""

from dataclasses import dataclass
from statistics import mean
from typing import Iterable

from benchmarks.brand_naming.intent_metrics import (
    IntentQualityMetrics,
    evaluate_intent_quality,
)
from benchmarks.brand_naming.intent_runner import ProjectOriginIntentRunner
from benchmarks.brand_naming.loader import load_cases
from benchmarks.brand_naming.metrics import (
    HardConstraintMetrics,
    evaluate_hard_constraints,
)
from benchmarks.brand_naming.models import BrandNamingBenchmarkCase
from benchmarks.brand_naming.project_origin_runner import (
    ProjectOriginNamingRunner,
)
from benchmarks.brand_naming.results import (
    BrandIntentBenchmarkOutput,
    BrandNamingBenchmarkOutput,
)
from project_origin.brand.intent import LlmBrandIntentInterpreter
from project_origin.llm.base import LLMProvider
from project_origin.llm.mock_provider import MockProvider


@dataclass(frozen=True)
class BrandBenchmarkCaseReport:
    case_id: str
    naming_output: BrandNamingBenchmarkOutput
    naming_metrics: HardConstraintMetrics
    intent_output: BrandIntentBenchmarkOutput
    active_intent_metrics: IntentQualityMetrics
    llm_intent_metrics: IntentQualityMetrics | None = None

    def to_dict(self) -> dict:
        return {
            "case_id": self.case_id,
            "naming_output": self.naming_output.to_dict(),
            "naming_metrics": _hard_metrics_to_dict(self.naming_metrics),
            "intent_output": self.intent_output.to_dict(),
            "active_intent_metrics": _intent_metrics_to_dict(
                self.active_intent_metrics
            ),
            "llm_intent_metrics": (
                _intent_metrics_to_dict(self.llm_intent_metrics)
                if self.llm_intent_metrics is not None
                else None
            ),
        }


@dataclass(frozen=True)
class BrandBenchmarkSuiteReport:
    approach: str
    cases: tuple[BrandBenchmarkCaseReport, ...]

    def to_dict(self) -> dict:
        return {
            "approach": self.approach,
            "summary": self.summary(),
            "cases": [case.to_dict() for case in self.cases],
        }

    def summary(self) -> dict:
        naming_metrics = [case.naming_metrics for case in self.cases]
        active_metrics = [case.active_intent_metrics for case in self.cases]
        llm_metrics = [
            case.llm_intent_metrics
            for case in self.cases
            if case.llm_intent_metrics is not None
        ]

        return {
            "case_count": len(self.cases),
            "naming_hard_constraint_pass_rate": _pass_rate(
                metric.passed for metric in naming_metrics
            ),
            "active_intent": _intent_summary(active_metrics),
            "llm_shadow_intent": (
                _intent_summary(llm_metrics) if llm_metrics else None
            ),
        }


class BrandBenchmarkSuite:
    def __init__(
        self,
        naming_runner: ProjectOriginNamingRunner | None = None,
        llm_provider: LLMProvider | None = None,
    ) -> None:
        self.naming_runner = naming_runner or ProjectOriginNamingRunner()
        self.intent_runner = ProjectOriginIntentRunner(
            llm=(
                LlmBrandIntentInterpreter(llm_provider)
                if llm_provider is not None
                else None
            )
        )

    @classmethod
    def with_mock_llm(cls) -> "BrandBenchmarkSuite":
        return cls(llm_provider=MockProvider())

    def run(
        self,
        cases: Iterable[BrandNamingBenchmarkCase] | None = None,
    ) -> BrandBenchmarkSuiteReport:
        loaded_cases = tuple(cases) if cases is not None else load_cases()
        reports = tuple(self._run_case(case) for case in loaded_cases)
        return BrandBenchmarkSuiteReport(
            approach="project_origin_structured_pipeline",
            cases=reports,
        )

    def _run_case(
        self,
        case: BrandNamingBenchmarkCase,
    ) -> BrandBenchmarkCaseReport:
        naming_output = self.naming_runner.run(case)
        naming_metrics = evaluate_hard_constraints(case, naming_output)

        intent_output = self.intent_runner.run(case)
        active_metrics = evaluate_intent_quality(
            case,
            intent_output.active_signals,
        )
        llm_metrics = None
        if intent_output.llm_candidate_signals:
            llm_metrics = evaluate_intent_quality(
                case,
                intent_output.llm_candidate_signals,
            )

        return BrandBenchmarkCaseReport(
            case_id=case.identifier,
            naming_output=naming_output,
            naming_metrics=naming_metrics,
            intent_output=intent_output,
            active_intent_metrics=active_metrics,
            llm_intent_metrics=llm_metrics,
        )


def _hard_metrics_to_dict(metrics: HardConstraintMetrics) -> dict:
    return {
        "candidate_count": metrics.candidate_count,
        "has_exactly_five_candidates": metrics.has_exactly_five_candidates,
        "forbidden_term_violations": metrics.forbidden_term_violations,
        "passed": metrics.passed,
    }


def _intent_metrics_to_dict(metrics: IntentQualityMetrics) -> dict:
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


def _intent_summary(metrics: list[IntentQualityMetrics]) -> dict:
    if not metrics:
        return {
            "average_strict_concept_coverage": 0.0,
            "average_relaxed_concept_coverage": 0.0,
            "average_evidence_hint_coverage": 0.0,
            "grounding_pass_rate": 0.0,
            "known_bad_pattern_violation_count": 0,
        }

    return {
        "average_strict_concept_coverage": mean(
            metric.expected_concept_coverage for metric in metrics
        ),
        "average_relaxed_concept_coverage": mean(
            metric.relaxed_concept_coverage for metric in metrics
        ),
        "average_evidence_hint_coverage": mean(
            metric.evidence_hint_coverage for metric in metrics
        ),
        "grounding_pass_rate": _pass_rate(
            metric.passed_grounding for metric in metrics
        ),
        "known_bad_pattern_violation_count": sum(
            len(metric.known_bad_pattern_violations) for metric in metrics
        ),
    }


def _pass_rate(values: Iterable[bool]) -> float:
    values = tuple(values)
    if not values:
        return 0.0
    return sum(1 for value in values if value) / len(values)
