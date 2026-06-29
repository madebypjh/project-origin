"""Analyze reviewed brand list candidates into Brand Genome batch files."""

from __future__ import annotations

from argparse import ArgumentParser
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re

from project_origin.llm.base import LLMProvider
from project_origin.llm.factory import LLMFactory
from research.brand_analyzer import BrandAnalyzer


@dataclass(frozen=True)
class CandidateAnalysisBatch:
    category: str
    batch_index: int
    brands: tuple[str, ...]
    output_path: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CandidateAnalysisRunReport:
    source_path: str
    batch_size: int
    analyzed_brand_count: int
    batches: tuple[CandidateAnalysisBatch, ...]

    def to_dict(self) -> dict:
        return {
            "source_path": self.source_path,
            "batch_size": self.batch_size,
            "analyzed_brand_count": self.analyzed_brand_count,
            "batches": [batch.to_dict() for batch in self.batches],
        }


class BrandCandidateBatchAnalyzer:
    DEFAULT_INPUT_PATH = (
        Path("dataset") / "analysis" / "brand_list_reviewed.json"
    )
    DEFAULT_REPORT_PATH = (
        Path("dataset") / "analysis" / "brand_candidate_analysis_report.json"
    )

    def __init__(
        self,
        provider: LLMProvider | None = None,
        output_dir: Path | None = None,
    ) -> None:
        self.project_root = Path(__file__).resolve().parents[1]
        self.output_dir = output_dir or self.project_root / "dataset" / "analysis"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.analyzer = BrandAnalyzer(
            provider=provider,
            output_dir=self.output_dir,
        )

    def analyze_reviewed_candidates(
        self,
        input_path: Path | None = None,
        categories: tuple[str, ...] = (),
        batch_size: int = 10,
        max_brands: int | None = None,
        report_path: Path | None = None,
    ) -> CandidateAnalysisRunReport:
        if batch_size <= 0:
            raise ValueError("batch_size must be positive")
        if max_brands is not None and max_brands <= 0:
            raise ValueError("max_brands must be positive when provided")

        source_path = self._resolve_path(input_path or self.DEFAULT_INPUT_PATH)
        accepted = self._load_accepted(source_path, categories)
        batches = []
        analyzed_count = 0

        for category, brands in accepted.items():
            remaining_slots = (
                None if max_brands is None else max_brands - analyzed_count
            )
            if remaining_slots is not None and remaining_slots <= 0:
                break
            selected_brands = (
                brands
                if remaining_slots is None
                else brands[:remaining_slots]
            )
            for batch_index, batch in enumerate(
                self._chunks(selected_brands, batch_size),
                start=1,
            ):
                filename = (
                    "brand_genome_candidates_"
                    f"{self._slug(category)}_batch_{batch_index:03d}.json"
                )
                output_path = self.analyzer.analyze(list(batch), filename)
                batches.append(
                    CandidateAnalysisBatch(
                        category=category,
                        batch_index=batch_index,
                        brands=batch,
                        output_path=str(output_path),
                    )
                )
                analyzed_count += len(batch)
                if max_brands is not None and analyzed_count >= max_brands:
                    break

        report = CandidateAnalysisRunReport(
            source_path=str(source_path),
            batch_size=batch_size,
            analyzed_brand_count=analyzed_count,
            batches=tuple(batches),
        )
        self._write_report(report, report_path)
        return report

    def _load_accepted(
        self,
        source_path: Path,
        categories: tuple[str, ...],
    ) -> dict[str, tuple[str, ...]]:
        data = json.loads(source_path.read_text(encoding="utf-8"))
        if data.get("status") != "reviewed_by_rules_requires_optional_human_review":
            raise ValueError(
                "reviewed brand list must have status "
                "reviewed_by_rules_requires_optional_human_review"
            )
        accepted = data.get("accepted")
        if not isinstance(accepted, dict):
            raise ValueError("reviewed brand list must contain accepted brands")

        requested = {category.casefold(): category for category in categories}
        selected = {}
        for category, brands in accepted.items():
            if requested and category.casefold() not in requested:
                continue
            if not isinstance(brands, list) or not all(
                isinstance(brand, str) and brand.strip()
                for brand in brands
            ):
                raise ValueError(f"{category} accepted brands must be strings")
            selected[category] = tuple(brand.strip() for brand in brands)

        if not selected:
            raise ValueError("no accepted brands matched the requested categories")
        return selected

    def _write_report(
        self,
        report: CandidateAnalysisRunReport,
        report_path: Path | None,
    ) -> None:
        destination = self._resolve_path(report_path or self.DEFAULT_REPORT_PATH)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(report.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _resolve_path(self, path: Path) -> Path:
        return path if path.is_absolute() else self.project_root / path

    @staticmethod
    def _chunks(
        values: tuple[str, ...],
        size: int,
    ) -> tuple[tuple[str, ...], ...]:
        return tuple(
            values[index : index + size]
            for index in range(0, len(values), size)
        )

    @staticmethod
    def _slug(value: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")
        return slug or "unknown"


def main() -> None:
    parser = ArgumentParser(
        description="Analyze reviewed brand candidates into Brand Genome JSON."
    )
    parser.add_argument("--provider", default="openai", choices=("openai", "mock"))
    parser.add_argument("--category", action="append", default=[])
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--max-brands", type=int)
    args = parser.parse_args()

    analyzer = BrandCandidateBatchAnalyzer(
        provider=LLMFactory.create(args.provider),
    )
    report = analyzer.analyze_reviewed_candidates(
        categories=tuple(args.category),
        batch_size=args.batch_size,
        max_brands=args.max_brands,
    )
    print(
        "Analyzed "
        f"{report.analyzed_brand_count} brands across {len(report.batches)} batches."
    )


if __name__ == "__main__":
    main()
