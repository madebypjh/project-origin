"""Validate and promote AI-proposed Brand List candidates.

AI-generated brand lists are not research data until they pass this review
gate. The reviewer produces a deterministic audit trail with accepted and
rejected candidates plus rejection reasons.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re

from research.collector import BrandCollector


@dataclass(frozen=True)
class BrandCandidateReviewItem:
    category: str
    name: str
    status: str
    reasons: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class BrandCandidateReviewReport:
    source_path: str
    accepted: dict[str, tuple[str, ...]]
    rejected: tuple[BrandCandidateReviewItem, ...]

    @property
    def accepted_count(self) -> int:
        return sum(len(brands) for brands in self.accepted.values())

    @property
    def rejected_count(self) -> int:
        return len(self.rejected)

    def to_dict(self) -> dict:
        return {
            "status": "reviewed_by_rules_requires_optional_human_review",
            "source_path": self.source_path,
            "summary": {
                "accepted_count": self.accepted_count,
                "rejected_count": self.rejected_count,
            },
            "accepted": {
                category: list(brands)
                for category, brands in self.accepted.items()
            },
            "rejected": [item.to_dict() for item in self.rejected],
        }


class BrandListCandidateReviewer:
    DEFAULT_INPUT_PATH = (
        Path("dataset") / "analysis" / "brand_list_candidates.json"
    )
    DEFAULT_OUTPUT_PATH = (
        Path("dataset") / "analysis" / "brand_list_reviewed.json"
    )

    MOJIBAKE_MARKERS = ("챕", "�", "ì", "Ã", "Â")
    LEGAL_SUFFIXES = (
        " inc",
        " inc.",
        " llc",
        " ltd",
        " ltd.",
        " corp",
        " corp.",
        " corporation",
        " company",
        " co.",
    )

    def __init__(self) -> None:
        self.project_root = Path(__file__).resolve().parents[1]

    def review_file(
        self,
        input_path: Path | None = None,
        output_path: Path | None = None,
    ) -> Path:
        source_path = self._resolve_path(input_path or self.DEFAULT_INPUT_PATH)
        report = self.review(source_path)
        destination = self._resolve_path(output_path or self.DEFAULT_OUTPUT_PATH)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(report.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return destination

    def review(self, input_path: Path) -> BrandCandidateReviewReport:
        data = json.loads(input_path.read_text(encoding="utf-8"))
        self._validate_container(data)
        categories = data["categories"]

        accepted: dict[str, list[str]] = {
            category: [] for category in categories
        }
        rejected: list[BrandCandidateReviewItem] = []
        seen_global = {
            brand.casefold(): brand
            for brand in BrandCollector.get_all_brands()
        }

        for category, brands in categories.items():
            if not isinstance(category, str) or not category.strip():
                raise ValueError("category names must be non-empty strings")
            if not isinstance(brands, list):
                raise ValueError(f"{category} must contain a list of brands")

            for raw_name in brands:
                cleaned = self._clean_name(raw_name)
                reasons = self._rejection_reasons(cleaned, raw_name)
                normalized = cleaned.casefold()

                if normalized in seen_global:
                    reasons.append("duplicate_existing_or_cross_category")

                if reasons:
                    rejected.append(
                        BrandCandidateReviewItem(
                            category=category,
                            name=cleaned or str(raw_name),
                            status="rejected",
                            reasons=tuple(dict.fromkeys(reasons)),
                        )
                    )
                    continue

                accepted[category].append(cleaned)
                seen_global[normalized] = cleaned

        return BrandCandidateReviewReport(
            source_path=str(input_path),
            accepted={
                category: tuple(brands)
                for category, brands in accepted.items()
            },
            rejected=tuple(rejected),
        )

    def _resolve_path(self, path: Path) -> Path:
        return path if path.is_absolute() else self.project_root / path

    @staticmethod
    def _validate_container(data: dict) -> None:
        if not isinstance(data, dict):
            raise ValueError("brand list candidate file must be an object")
        if data.get("status") != "candidate_only_requires_review":
            raise ValueError(
                "brand list candidate file must have status "
                "candidate_only_requires_review"
            )
        if not isinstance(data.get("categories"), dict):
            raise ValueError("brand list candidate file must contain categories")

    @classmethod
    def _rejection_reasons(cls, cleaned: str, raw_name) -> list[str]:
        reasons = []
        if not isinstance(raw_name, str):
            reasons.append("not_a_string")
        if not cleaned:
            reasons.append("empty_or_invalid")
            return reasons
        if any(marker in cleaned for marker in cls.MOJIBAKE_MARKERS):
            reasons.append("encoding_suspect")
        if "://" in cleaned or "/" in cleaned:
            reasons.append("url_or_path")
        if len(cleaned) > 40:
            reasons.append("too_long")
        if cls._looks_like_legal_entity(cleaned):
            reasons.append("legal_entity_name")
        if not re.search(r"[A-Za-z0-9]", cleaned):
            reasons.append("no_latin_or_numeric_character")
        return reasons

    @classmethod
    def _looks_like_legal_entity(cls, name: str) -> bool:
        normalized = name.casefold().strip()
        return any(normalized.endswith(suffix) for suffix in cls.LEGAL_SUFFIXES)

    @staticmethod
    def _clean_name(value) -> str:
        if not isinstance(value, str):
            return ""
        return " ".join(value.strip().split())


def main() -> None:
    reviewer = BrandListCandidateReviewer()
    output_path = reviewer.review_file()
    print(f"Brand list review saved to: {output_path}")


if __name__ == "__main__":
    main()
