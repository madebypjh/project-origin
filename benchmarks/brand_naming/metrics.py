"""Objective checks that do not depend on a model-as-judge."""

from dataclasses import dataclass
import re

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


@dataclass(frozen=True)
class CaseAwareNamingMetrics:
    required_quality_coverage: float
    selected_required_quality_coverage: float
    matched_required_qualities: tuple[str, ...]
    missing_required_qualities: tuple[str, ...]
    known_bad_pattern_violations: tuple[str, ...]
    average_risk_score: float
    selected_risk_score: float
    score_margin: float | None
    low_confidence_decision: bool


@dataclass(frozen=True)
class DecisionEvidenceMetrics:
    has_score_delta: bool
    has_strategy_delta: bool
    has_tradeoff: bool
    has_risk_assessment: bool
    has_report_foundation: bool
    completeness: float


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


def evaluate_case_aware_naming(
    case: BrandNamingBenchmarkCase,
    output: BrandNamingBenchmarkOutput,
) -> CaseAwareNamingMetrics:
    evaluations = _evaluations_by_name(output)
    selected = evaluations.get(output.selected_name.casefold(), {})
    selected_scores = selected.get("scores", {})

    matched_required_qualities = tuple(
        quality
        for quality in case.required_qualities
        if _quality_matched(quality, selected_scores)
    )
    missing_required_qualities = tuple(
        quality
        for quality in case.required_qualities
        if quality not in matched_required_qualities
    )
    selected_required_quality_coverage = _coverage(
        len(matched_required_qualities),
        len(case.required_qualities),
    )

    all_quality_hits = 0
    all_quality_slots = len(case.required_qualities) * len(output.candidates)
    for candidate in output.candidates:
        scores = evaluations.get(candidate.casefold(), {}).get("scores", {})
        all_quality_hits += sum(
            1
            for quality in case.required_qualities
            if _quality_matched(quality, scores)
        )

    risk_scores = [
        _candidate_risk_score(case, candidate, output.reasoning)
        for candidate in output.candidates
    ]
    selected_risk_score = _candidate_risk_score(
        case,
        output.selected_name,
        output.reasoning,
    )
    known_bad_pattern_violations = tuple(
        violation
        for candidate in output.candidates
        for violation in _known_bad_pattern_violations(
            case,
            candidate,
            output.reasoning,
        )
    )
    score_margin = _score_margin(output)
    low_confidence_decision = (
        selected_required_quality_coverage < 0.67
        or selected_risk_score >= 0.25
        or (score_margin is not None and score_margin < 0.15)
    )

    return CaseAwareNamingMetrics(
        required_quality_coverage=_coverage(
            all_quality_hits,
            all_quality_slots,
        ),
        selected_required_quality_coverage=selected_required_quality_coverage,
        matched_required_qualities=matched_required_qualities,
        missing_required_qualities=missing_required_qualities,
        known_bad_pattern_violations=known_bad_pattern_violations,
        average_risk_score=round(
            sum(risk_scores) / len(risk_scores) if risk_scores else 0.0,
            4,
        ),
        selected_risk_score=selected_risk_score,
        score_margin=score_margin,
        low_confidence_decision=low_confidence_decision,
    )


def evaluate_decision_evidence(
    output: BrandNamingBenchmarkOutput,
) -> DecisionEvidenceMetrics:
    evidence = output.decision_evidence
    checks = {
        "has_score_delta": evidence.get("score_delta") is not None,
        "has_strategy_delta": evidence.get("strategy_delta") is not None,
        "has_tradeoff": bool(evidence.get("runner_up_tradeoffs")),
        "has_risk_assessment": bool(evidence.get("risk_assessment")),
        "has_report_foundation": bool(
            evidence.get("brand_history_seed")
            and evidence.get("brand_dna")
            and evidence.get("value_alignment")
        ),
    }

    return DecisionEvidenceMetrics(
        **checks,
        completeness=_coverage(
            sum(1 for passed in checks.values() if passed),
            len(checks),
        ),
    )


def _evaluations_by_name(
    output: BrandNamingBenchmarkOutput,
) -> dict[str, dict]:
    return {
        str(evaluation.get("name", "")).casefold(): evaluation
        for evaluation in output.candidate_evaluations
    }


def _quality_matched(quality: str, scores: dict) -> bool:
    normalized_quality = _normalize_text(quality)
    pronunciation = float(scores.get("pronunciation", 0.0))
    originality = float(scores.get("originality", 0.0))
    strategic_fit = float(scores.get("strategic_fit", 0.0))
    memorability = float(scores.get("memorability", 0.0))

    if normalized_quality in {
        "globally pronounceable",
        "simple",
        "calm",
        "non clinical",
    }:
        return pronunciation >= 8.0

    if normalized_quality in {"memorable", "human", "warm", "expressive"}:
        return memorability >= 8.0 and originality >= 7.0

    if normalized_quality in {
        "credible",
        "precise",
        "confident",
        "professional",
        "grounded",
        "durable",
        "industrial",
    }:
        return strategic_fit >= 7.5

    return strategic_fit >= 7.5 or originality >= 8.0


def _candidate_risk_score(
    case: BrandNamingBenchmarkCase,
    candidate: str,
    reasoning: str,
) -> float:
    risk = 0.0
    normalized_candidate = _normalize_text(candidate)

    for term in case.forbidden_terms:
        if _normalize_text(term) in normalized_candidate:
            risk += 0.5

    risk += 0.25 * len(
        _known_bad_pattern_violations(case, candidate, reasoning)
    )

    generic_fragments = {
        "ai",
        "bot",
        "brand",
        "content",
        "generator",
        "group",
        "labs",
        "solution",
        "tech",
    }
    if any(fragment in normalized_candidate for fragment in generic_fragments):
        risk += 0.1

    return round(min(risk, 1.0), 4)


def _known_bad_pattern_violations(
    case: BrandNamingBenchmarkCase,
    candidate: str,
    reasoning: str,
) -> tuple[str, ...]:
    text = _normalize_text(f"{candidate} {reasoning}")
    violations = []
    for pattern in case.known_bad_patterns:
        if _pattern_matched(pattern, text):
            violations.append(f"{candidate}: {pattern}")
    return tuple(violations)


def _pattern_matched(pattern: str, text: str) -> bool:
    normalized_pattern = _normalize_text(pattern)
    if normalized_pattern in text:
        return True

    risk_terms_by_pattern = {
        "automation": {"auto", "bot", "generator"},
        "banking": {"bank", "capital", "coin", "crypto"},
        "clinical": {"clinic", "cure", "diagnose", "doctor", "med"},
        "content": {"bot", "content", "generator"},
        "crypto": {"coin", "crypto"},
        "cure": {"cure"},
        "eco": {"eco", "green", "planet"},
        "fear": {"breach", "fear", "hack", "threat"},
        "greenwashing": {"eco", "green", "planet"},
        "hacker": {"hack"},
    }
    pattern_tokens = set(normalized_pattern.split())
    risk_terms = set()
    for token in pattern_tokens:
        risk_terms.update(risk_terms_by_pattern.get(token, set()))

    tokens = set(text.split())
    return any(_risk_term_matched(term, tokens) for term in risk_terms)


def _risk_term_matched(term: str, tokens: set[str]) -> bool:
    if term in tokens:
        return True

    prefix_terms = {
        "auto",
        "bank",
        "breach",
        "clinic",
        "crypto",
        "cure",
        "diagnose",
        "doctor",
        "fear",
        "generator",
        "green",
        "hack",
        "planet",
        "threat",
    }
    if term not in prefix_terms:
        return False

    return any(token.startswith(term) for token in tokens)


def _score_margin(output: BrandNamingBenchmarkOutput) -> float | None:
    scores = sorted(
        (
            float(evaluation.get("total_score", 0.0))
            for evaluation in output.candidate_evaluations
        ),
        reverse=True,
    )
    if len(scores) < 2:
        return None
    return round(scores[0] - scores[1], 2)


def _coverage(matches: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round(matches / total, 4)


def _normalize_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()
