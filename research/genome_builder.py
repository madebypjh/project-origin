"""
Project Origin - Genome Builder

Combines validated Brand Genome analysis files into one dataset.
"""

import json
from pathlib import Path

from research.normalizer import BrandGenomeNormalizer
from research.validator import BrandGenomeValidator


class BrandGenomeBuilder:
    def __init__(self) -> None:
        self.project_root = Path(__file__).resolve().parents[1]
        self.analysis_dir = self.project_root / "dataset" / "analysis"
        self.output_path = self.project_root / "dataset" / "brand_genome.json"

    def build(self) -> Path:
        genome = []

        for file_path in sorted(self.analysis_dir.glob("*brand_genome*.json")):
            data = json.loads(file_path.read_text(encoding="utf-8"))

            normalized = BrandGenomeNormalizer.normalize_many(data)
            errors = BrandGenomeValidator.validate_many(normalized)

            if errors:
                raise ValueError(
                    f"Validation failed in {file_path.name}: {errors}"
                )

            genome.extend(normalized)

        genome = self._deduplicate_by_name(genome)

        self.output_path.write_text(
            json.dumps(genome, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return self.output_path

    @staticmethod
    def _deduplicate_by_name(items: list[dict]) -> list[dict]:
        deduplicated = {}

        for item in items:
            name = item["name"].lower().strip()
            deduplicated[name] = item

        return list(deduplicated.values())


def main() -> None:
    builder = BrandGenomeBuilder()
    output_path = builder.build()
    print(f"Brand Genome built: {output_path}")


if __name__ == "__main__":
    main()