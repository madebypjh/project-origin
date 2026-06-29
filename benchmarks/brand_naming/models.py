"""Typed inputs for comparing Brand naming decision approaches."""

from dataclasses import dataclass
from typing import Any

from project_origin.brand.models import FounderProfile


@dataclass(frozen=True)
class BrandNamingBenchmarkCase:
    identifier: str
    profile: FounderProfile
    expected_themes: tuple[str, ...]
    required_qualities: tuple[str, ...]
    forbidden_terms: tuple[str, ...]
    evaluation_notes: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BrandNamingBenchmarkCase":
        required_fields = {
            "id",
            "profile",
            "expected_themes",
            "required_qualities",
            "forbidden_terms",
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
            evaluation_notes=str(data.get("evaluation_notes", "")).strip(),
        )
        if not case.identifier:
            raise ValueError("Benchmark case id must not be empty")
        if not case.expected_themes:
            raise ValueError("Benchmark case must define expected_themes")
        if not case.required_qualities:
            raise ValueError("Benchmark case must define required_qualities")
        return case

    @staticmethod
    def _string_tuple(value: Any, field_name: str) -> tuple[str, ...]:
        if not isinstance(value, list) or not all(
            isinstance(item, str) and item.strip()
            for item in value
        ):
            raise ValueError(f"{field_name} must be a list of non-empty strings")
        return tuple(item.strip() for item in value)
