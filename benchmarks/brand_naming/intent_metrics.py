"""Intent quality metrics for Brand benchmark cases."""

from dataclasses import dataclass
import re

from benchmarks.brand_naming.models import BrandNamingBenchmarkCase
from benchmarks.brand_naming.results import IntentBenchmarkSignal
from project_origin.brand.intent.adapter import BrandIntentAdapter


@dataclass(frozen=True)
class IntentQualityMetrics:
    expected_signal_count: int
    signal_count: int
    expected_concept_matches: tuple[str, ...]
    relaxed_concept_matches: tuple[str, ...]
    expected_evidence_matches: tuple[str, ...]
    missing_expected_concepts: tuple[str, ...]
    relaxed_missing_expected_concepts: tuple[str, ...]
    unsupported_evidence: tuple[str, ...]
    known_bad_pattern_violations: tuple[str, ...]

    @property
    def expected_concept_coverage(self) -> float:
        if self.expected_signal_count == 0:
            return 0.0
        return len(self.expected_concept_matches) / self.expected_signal_count

    @property
    def relaxed_concept_coverage(self) -> float:
        if self.expected_signal_count == 0:
            return 0.0
        return len(self.relaxed_concept_matches) / self.expected_signal_count

    @property
    def evidence_hint_coverage(self) -> float:
        if self.expected_signal_count == 0:
            return 0.0
        return len(self.expected_evidence_matches) / self.expected_signal_count

    @property
    def passed_grounding(self) -> bool:
        return not self.unsupported_evidence


def evaluate_intent_quality(
    case: BrandNamingBenchmarkCase,
    signals: tuple[IntentBenchmarkSignal, ...],
) -> IntentQualityMetrics:
    source_text = _normalize_text(BrandIntentAdapter.source_text(case.profile))
    actual_concepts = {_normalize_identifier(signal.concept) for signal in signals}
    expected_concepts = tuple(
        _normalize_identifier(signal.concept)
        for signal in case.expected_intent_signals
    )
    expected_evidence_matches = []
    expected_concept_matches = []
    relaxed_concept_matches = []

    for expected in case.expected_intent_signals:
        concept = _normalize_identifier(expected.concept)
        if concept in actual_concepts:
            expected_concept_matches.append(expected.concept)
        if _relaxed_concept_matched(concept, actual_concepts):
            relaxed_concept_matches.append(expected.concept)
        if _evidence_hint_matched(expected.evidence_hint, signals):
            expected_evidence_matches.append(expected.concept)

    missing_expected_concepts = tuple(
        expected.concept
        for expected in case.expected_intent_signals
        if _normalize_identifier(expected.concept) not in actual_concepts
    )
    relaxed_missing_expected_concepts = tuple(
        expected.concept
        for expected in case.expected_intent_signals
        if not _relaxed_concept_matched(
            _normalize_identifier(expected.concept),
            actual_concepts,
        )
    )
    unsupported_evidence = []
    for signal in signals:
        for evidence in signal.evidence:
            if _normalize_text(evidence) not in source_text:
                unsupported_evidence.append(f"{signal.concept}: {evidence}")

    known_bad_pattern_violations = []
    signal_text = _normalize_text(
        " ".join(
            [
                " ".join(signal.evidence)
                + " "
                + signal.concept
                + " "
                + signal.kind
                for signal in signals
            ]
        )
    )
    for pattern in case.known_bad_patterns:
        if _normalize_text(pattern) in signal_text:
            known_bad_pattern_violations.append(pattern)

    return IntentQualityMetrics(
        expected_signal_count=len(case.expected_intent_signals),
        signal_count=len(signals),
        expected_concept_matches=tuple(expected_concept_matches),
        relaxed_concept_matches=tuple(relaxed_concept_matches),
        expected_evidence_matches=tuple(expected_evidence_matches),
        missing_expected_concepts=missing_expected_concepts,
        relaxed_missing_expected_concepts=relaxed_missing_expected_concepts,
        unsupported_evidence=tuple(unsupported_evidence),
        known_bad_pattern_violations=tuple(known_bad_pattern_violations),
    )


def _evidence_hint_matched(
    evidence_hint: str,
    signals: tuple[IntentBenchmarkSignal, ...],
) -> bool:
    normalized_hint = _normalize_text(evidence_hint)
    return any(
        normalized_hint in _normalize_text(evidence)
        for signal in signals
        for evidence in signal.evidence
    )


def _relaxed_concept_matched(
    expected_concept: str,
    actual_concepts: set[str],
) -> bool:
    expected_tokens = _concept_tokens(expected_concept)
    if not expected_tokens:
        return False

    for actual_concept in actual_concepts:
        if expected_concept == actual_concept:
            return True
        if expected_concept in actual_concept:
            return True
        actual_tokens = _concept_tokens(actual_concept)
        if expected_tokens.issubset(actual_tokens):
            return True

    return False


def _concept_tokens(value: str) -> set[str]:
    return {
        _normalize_concept_token(token)
        for token in _normalize_identifier(value).split("_")
        if token and token not in {"and", "for", "of", "the", "to", "with"}
    }


def _normalize_concept_token(token: str) -> str:
    priority_variants = {
        "priorities": "priority",
        "prioritization": "priority",
        "prioritisation": "priority",
        "prioritize": "priority",
        "prioritise": "priority",
    }
    if token in priority_variants:
        return priority_variants[token]
    if token.endswith("ies") and len(token) > 4:
        return token[:-3] + "y"
    if token.endswith("s") and len(token) > 3:
        return token[:-1]
    return token


def _normalize_identifier(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")
    return re.sub(r"_+", "_", normalized)


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()
