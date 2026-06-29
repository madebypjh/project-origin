"""
Project Origin - Research Normalizer

Normalizes Brand Genome JSON before validation.
"""


class BrandGenomeNormalizer:
    STYLE_ALIASES = {
        "invented word": "invented",
        "coined": "invented",
        "coined word": "invented",
        "blend": "blended",
        "compound word": "descriptive",
        "symbol": "symbolic",
    }

    SEMANTIC_DENSITY_ALIASES = {
        "no": "none",
        "none": "none",
        "low": "low",
        "medium": "medium",
        "high": "high",
    }

    @classmethod
    def normalize_many(cls, items: list[dict]) -> list[dict]:
        return [cls.normalize_item(item) for item in items]

    @classmethod
    def normalize_item(cls, item: dict) -> dict:
        normalized = dict(item)

        cls._normalize_text_fields(normalized)
        cls._normalize_style(normalized)
        cls._normalize_semantic_density(normalized)
        cls._normalize_scores(normalized)
        cls._normalize_ratios(normalized)
        cls._normalize_syllables(normalized)

        return normalized

    @staticmethod
    def _normalize_text_fields(item: dict) -> None:
        for key, value in list(item.items()):
            if isinstance(value, str):
                item[key] = value.strip()

    @classmethod
    def _normalize_style(cls, item: dict) -> None:
        style = item.get("style")

        if not isinstance(style, str):
            return

        normalized_style = style.strip().lower()
        item["style"] = cls.STYLE_ALIASES.get(normalized_style, normalized_style)

    @classmethod
    def _normalize_semantic_density(cls, item: dict) -> None:
        density = item.get("semantic_density")

        if not isinstance(density, str):
            return

        normalized_density = density.strip().lower()
        item["semantic_density"] = cls.SEMANTIC_DENSITY_ALIASES.get(
            normalized_density,
            normalized_density,
        )

    @staticmethod
    def _normalize_scores(item: dict) -> None:
        score_fields = [
            "pronunciation_difficulty",
            "memorability_score",
            "distinctiveness_score",
            "innovation_score",
            "trust_score",
            "premium_score",
            "playfulness_score",
            "global_scalability_score",
        ]

        for field in score_fields:
            value = item.get(field)

            if isinstance(value, str):
                try:
                    value = float(value)
                except ValueError:
                    continue

            if isinstance(value, (int, float)):
                item[field] = max(0, min(10, value))

    @staticmethod
    def _normalize_ratios(item: dict) -> None:
        ratio_fields = [
            "vowel_ratio",
            "hard_consonant_ratio",
            "soft_consonant_ratio",
        ]

        for field in ratio_fields:
            value = item.get(field)

            if isinstance(value, str):
                try:
                    value = float(value)
                except ValueError:
                    continue

            if isinstance(value, (int, float)):
                item[field] = max(0, min(1, value))

    @staticmethod
    def _normalize_syllables(item: dict) -> None:
        syllables = item.get("syllables")

        if isinstance(syllables, str):
            item["syllables"] = [
                part.strip()
                for part in syllables.split(",")
                if part.strip()
            ]