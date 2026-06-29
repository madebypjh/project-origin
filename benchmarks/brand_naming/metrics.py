"""Objective checks that do not depend on a model-as-judge."""

from dataclasses import dataclass

from benchmarks.brand_naming.models import BrandNamingBenchmarkCase
from benchmarks.brand_naming.results import BrandNamingBenchmarkOutput


@dataclass(frozen=True)
class HardConstraintMetrics:
    candidate_count: int
    has_exactly_five_candidates: bool
    forbidden_term_violations: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return (
            self.has_exactly_five_candidates
            and not self.forbidden_term_violations
        )


def evaluate_hard_constraints(
    case: BrandNamingBenchmarkCase,
    output: BrandNamingBenchmarkOutput,
) -> HardConstraintMetrics:
    violations = []
    for candidate in output.candidates:
        normalized_candidate = candidate.casefold()
        for term in case.forbidden_terms:
            if term.casefold() in normalized_candidate:
                violations.append(f"{candidate}: {term}")

    return HardConstraintMetrics(
        candidate_count=len(output.candidates),
        has_exactly_five_candidates=len(output.candidates) == 5,
        forbidden_term_violations=tuple(violations),
    )
