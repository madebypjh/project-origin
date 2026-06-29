"""
Project Origin - Pattern Extractor

Extracts statistical naming patterns from Brand Genome data.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean


class PatternExtractor:
    def __init__(self) -> None:
        self.project_root = Path(__file__).resolve().parents[1]
        self.genome_path = self.project_root / "dataset" / "brand_genome.json"
        self.output_path = self.project_root / "dataset" / "analysis" / "brand_patterns.json"

    def extract(self) -> Path:
        genome = self._load_genome()

        patterns = {
            "global": self._extract_group_patterns(genome),
            "by_industry": self._extract_industry_patterns(genome),
        }

        self.output_path.write_text(
            json.dumps(patterns, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return self.output_path

    def _load_genome(self) -> list[dict]:
        if not self.genome_path.exists():
            raise FileNotFoundError(
                "dataset/brand_genome.json not found. "
                "Run: python -m research.genome_builder"
            )

        return json.loads(self.genome_path.read_text(encoding="utf-8"))

    def _extract_industry_patterns(self, genome: list[dict]) -> dict:
        grouped = defaultdict(list)

        for item in genome:
            industry = item.get("industry", "unknown").lower().strip()
            grouped[industry].append(item)

        return {
            industry: self._extract_group_patterns(items)
            for industry, items in sorted(grouped.items())
        }

    def _extract_group_patterns(self, items: list[dict]) -> dict:
        if not items:
            return {}

        return {
            "sample_size": len(items),
            "average_name_length": self._average_name_length(items),
            "average_syllable_count": self._average_syllable_count(items),
            "average_vowel_ratio": self._average_numeric_field(items, "vowel_ratio"),
            "average_hard_consonant_ratio": self._average_numeric_field(
                items,
                "hard_consonant_ratio",
            ),
            "average_soft_consonant_ratio": self._average_numeric_field(
                items,
                "soft_consonant_ratio",
            ),
            "style_distribution": self._distribution(items, "style"),
            "semantic_density_distribution": self._distribution(
                items,
                "semantic_density",
            ),
            "archetype_distribution": self._distribution(items, "brand_archetype"),
            "emotional_tone_distribution": self._distribution(items, "emotional_tone"),
            "dominant_style": self._dominant_value(items, "style"),
            "dominant_archetype": self._dominant_value(items, "brand_archetype"),
            "dominant_emotional_tone": self._dominant_value(items, "emotional_tone"),
            "average_scores": {
                "memorability": self._average_numeric_field(
                    items,
                    "memorability_score",
                ),
                "distinctiveness": self._average_numeric_field(
                    items,
                    "distinctiveness_score",
                ),
                "innovation": self._average_numeric_field(
                    items,
                    "innovation_score",
                ),
                "trust": self._average_numeric_field(items, "trust_score"),
                "premium": self._average_numeric_field(items, "premium_score"),
                "playfulness": self._average_numeric_field(
                    items,
                    "playfulness_score",
                ),
                "global_scalability": self._average_numeric_field(
                    items,
                    "global_scalability_score",
                ),
            },
        }

    @staticmethod
    def _average_name_length(items: list[dict]) -> float:
        return round(mean(len(item.get("name", "")) for item in items), 2)

    @staticmethod
    def _average_syllable_count(items: list[dict]) -> float:
        syllable_counts = [
            len(item.get("syllables", []))
            for item in items
            if isinstance(item.get("syllables"), list)
        ]

        if not syllable_counts:
            return 0.0

        return round(mean(syllable_counts), 2)

    @staticmethod
    def _average_numeric_field(items: list[dict], field: str) -> float:
        values = [
            item[field]
            for item in items
            if isinstance(item.get(field), (int, float))
        ]

        if not values:
            return 0.0

        return round(mean(values), 2)

    @staticmethod
    def _distribution(items: list[dict], field: str) -> dict[str, float]:
        values = [
            str(item.get(field, "unknown")).strip()
            for item in items
            if item.get(field) not in [None, ""]
        ]

        if not values:
            return {}

        counter = Counter(values)
        total = sum(counter.values())

        return {
            value: round(count / total, 2)
            for value, count in counter.most_common()
        }

    @staticmethod
    def _dominant_value(items: list[dict], field: str) -> str:
        values = [
            str(item.get(field, "unknown")).strip()
            for item in items
            if item.get(field) not in [None, ""]
        ]

        if not values:
            return "unknown"

        return Counter(values).most_common(1)[0][0]


def main() -> None:
    extractor = PatternExtractor()
    output_path = extractor.extract()

    print(f"Brand patterns extracted: {output_path}")


if __name__ == "__main__":
    main()