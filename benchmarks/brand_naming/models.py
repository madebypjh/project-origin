"""Typed inputs for comparing Brand naming decision approaches."""

from dataclasses import dataclass
from typing import Any

from project_origin.brand.models import FounderProfile


@dataclass(frozen=True)
class ExpectedIntentSignal:
    kind: str
    concept: str
    evidence_hint: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExpectedIntentSignal":
        required_fields = {"kind", "concept", "evidence_hint"}
        missing = sorted(required_fields - set(data))
        if missing:
            raise ValueError(
                "expected_intent_signals item is missing fields: "
                f"{', '.join(missing)}"
            )

        signal = cls(
            kind=str(data["kind"]).strip(),
            concept=str(data["concept"]).strip(),
            evidence_hint=str(data["evidence_hint"]).strip(),
        )
        if not signal.kind:
            raise ValueError("expected intent signal kind must not be empty")
        if not signal.concept:
            raise ValueError("expected intent signal concept must not be empty")
        if not signal.evidence_hint:
            raise ValueError(
                "expected intent signal evidence_hint must not be empty"
            )
        return signal


@dataclass(frozen=True)
class EvaluationRubric:
    strategic_fit: str
    distinctiveness: str
    trustworthiness: str
    explainability: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvaluationRubric":
        required_fields = {
            "strategic_fit",
            "distinctiveness",
            "trustworthiness",
            "explainability",
        }
        missing = sorted(required_fields - set(data))
        if missing:
            raise ValueError(
                f"evaluation_rubric is missing fields: {', '.join(missing)}"
            )

        rubric = cls(
            strategic_fit=str(data["strategic_fit"]).strip(),
            distinctiveness=str(data["distinctiveness"]).strip(),
            trustworthiness=str(data["trustworthiness"]).strip(),
            explainability=str(data["explainability"]).strip(),
        )
        if not all(
            (
                rubric.strategic_fit,
                rubric.distinctiveness,
                rubric.trustworthiness,
                rubric.explainability,
            )
        ):
            raise ValueError("evaluation_rubric values must not be empty")
        return rubric


@dataclass(frozen=True)
class BrandNamingBenchmarkCase:
    identifier: str
    profile: FounderProfile
    expected_themes: tuple[str, ...]
    required_qualities: tuple[str, ...]
    forbidden_terms: tuple[str, ...]
    expected_intent_signals: tuple[ExpectedIntentSignal, ...]
    known_bad_patterns: tuple[str, ...]
    evaluation_rubric: EvaluationRubric
    evaluation_notes: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BrandNamingBenchmarkCase":
        required_fields = {
            "id",
            "profile",
            "expected_themes",
            "required_qualities",
            "forbidden_terms",
            "expected_intent_signals",
            "known_bad_patterns",
            "evaluation_rubric",
        }
        missing = sorted(required_fields - set(data))
        if missing:
            raise ValueError(
                f"Benchmark case is missing fields: {', '.join(missing)}"
            )

        profile_data = data["profile"]
        if not isinstance(profile_data, dict):
            raise ValueError("Benchmark case profile must be an object")

        case = cls(
            identifier=str(data["id"]).strip(),
            profile=FounderProfile(**profile_data),
            expected_themes=cls._string_tuple(
                data["expected_themes"],
                "expected_themes",
            ),
            required_qualities=cls._string_tuple(
                data["required_qualities"],
                "required_qualities",
            ),
            forbidden_terms=cls._string_tuple(
                data["forbidden_terms"],
                "forbidden_terms",
            ),
            expected_intent_signals=cls._expected_signal_tuple(
                data["expected_intent_signals"],
            ),
            known_bad_patterns=cls._string_tuple(
                data["known_bad_patterns"],
                "known_bad_patterns",
            ),
            evaluation_rubric=cls._rubric(data["evaluation_rubric"]),
            evaluation_notes=str(data.get("evaluation_notes", "")).strip(),
        )
        if not case.identifier:
            raise ValueError("Benchmark case id must not be empty")
        if not case.expected_themes:
            raise ValueError("Benchmark case must define expected_themes")
        if not case.required_qualities:
            raise ValueError("Benchmark case must define required_qualities")
        if not case.expected_intent_signals:
            raise ValueError(
                "Benchmark case must define expected_intent_signals"
            )
        return case

    @staticmethod
    def _string_tuple(value: Any, field_name: str) -> tuple[str, ...]:
        if not isinstance(value, list) or not all(
            isinstance(item, str) and item.strip()
            for item in value
        ):
            raise ValueError(f"{field_name} must be a list of non-empty strings")
        return tuple(item.strip() for item in value)

    @staticmethod
    def _expected_signal_tuple(
        value: Any,
    ) -> tuple[ExpectedIntentSignal, ...]:
        if not isinstance(value, list):
            raise ValueError("expected_intent_signals must be a list")
        if not all(isinstance(item, dict) for item in value):
            raise ValueError(
                "expected_intent_signals must contain objects"
            )
        return tuple(ExpectedIntentSignal.from_dict(item) for item in value)

    @staticmethod
    def _rubric(value: Any) -> EvaluationRubric:
        if not isinstance(value, dict):
            raise ValueError("evaluation_rubric must be an object")
        return EvaluationRubric.from_dict(value)
