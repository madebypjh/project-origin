"""
Project Origin - Research Validator

Validates Brand Genome JSON produced by the research analyzer.
"""


class BrandGenomeValidator:
    REQUIRED_FIELDS = [
        "name",
        "industry",
        "country",
        "founded_year",
        "style",
        "name_origin",
        "semantic_density",
        "semantic_category",
        "brand_archetype",
        "emotional_tone",
        "phonetic_pattern",
        "syllables",
        "vowel_ratio",
        "hard_consonant_ratio",
        "soft_consonant_ratio",
        "pronunciation_difficulty",
        "memorability_score",
        "distinctiveness_score",
        "innovation_score",
        "trust_score",
        "premium_score",
        "playfulness_score",
        "global_scalability_score",
        "morphology_type",
        "linguistic_style",
        "notes",
    ]

    ALLOWED_STYLES = {
        "invented",
        "blended",
        "descriptive",
        "metaphorical",
        "acronym",
        "founder_name",
        "geographic",
        "latin",
        "greek",
        "abstract",
        "symbolic",
    }

    ALLOWED_SEMANTIC_DENSITY = {
        "none",
        "low",
        "medium",
        "high",
    }

    ALLOWED_ARCHETYPES = {
        "Sage",
        "Creator",
        "Explorer",
        "Hero",
        "Magician",
        "Caregiver",
        "Innocent",
        "Everyman",
        "Outlaw",
        "Jester",
        "Ruler",
        "Lover",
    }

    SCORE_FIELDS = [
        "pronunciation_difficulty",
        "memorability_score",
        "distinctiveness_score",
        "innovation_score",
        "trust_score",
        "premium_score",
        "playfulness_score",
        "global_scalability_score",
    ]

    RATIO_FIELDS = [
        "vowel_ratio",
        "hard_consonant_ratio",
        "soft_consonant_ratio",
    ]

    @classmethod
    def validate_many(cls, items: list[dict]) -> list[dict]:
        errors = []

        if not isinstance(items, list):
            raise ValueError("Brand genome data must be a list of objects.")

        for index, item in enumerate(items, start=1):
            item_errors = cls.validate_item(item)

            if item_errors:
                errors.append(
                    {
                        "index": index,
                        "name": item.get("name", "UNKNOWN")
                        if isinstance(item, dict)
                        else "INVALID_ITEM",
                        "errors": item_errors,
                    }
                )

        return errors

    @classmethod
    def validate_item(cls, item: dict) -> list[str]:
        errors = []

        if not isinstance(item, dict):
            return ["Item must be a JSON object."]

        errors.extend(cls._validate_required_fields(item))
        errors.extend(cls._validate_enums(item))
        errors.extend(cls._validate_scores(item))
        errors.extend(cls._validate_ratios(item))
        errors.extend(cls._validate_syllables(item))

        return errors

    @classmethod
    def _validate_required_fields(cls, item: dict) -> list[str]:
        return [
            f"Missing required field: {field}"
            for field in cls.REQUIRED_FIELDS
            if field not in item
        ]

    @classmethod
    def _validate_enums(cls, item: dict) -> list[str]:
        errors = []

        style = item.get("style")
        if style is not None and style not in cls.ALLOWED_STYLES:
            errors.append(f"Invalid style: {style}")

        semantic_density = item.get("semantic_density")
        if (
            semantic_density is not None
            and semantic_density not in cls.ALLOWED_SEMANTIC_DENSITY
        ):
            errors.append(f"Invalid semantic_density: {semantic_density}")

        archetype = item.get("brand_archetype")
        if archetype is not None and archetype not in cls.ALLOWED_ARCHETYPES:
            errors.append(f"Invalid brand_archetype: {archetype}")

        return errors

    @classmethod
    def _validate_scores(cls, item: dict) -> list[str]:
        errors = []

        for field in cls.SCORE_FIELDS:
            value = item.get(field)

            if value is None:
                continue

            if not isinstance(value, (int, float)):
                errors.append(f"{field} must be a number.")
                continue

            if value < 0 or value > 10:
                errors.append(f"{field} must be between 0 and 10.")

        return errors

    @classmethod
    def _validate_ratios(cls, item: dict) -> list[str]:
        errors = []

        for field in cls.RATIO_FIELDS:
            value = item.get(field)

            if value is None:
                continue

            if not isinstance(value, (int, float)):
                errors.append(f"{field} must be a number.")
                continue

            if value < 0 or value > 1:
                errors.append(f"{field} must be between 0 and 1.")

        return errors

    @staticmethod
    def _validate_syllables(item: dict) -> list[str]:
        syllables = item.get("syllables")

        if syllables is None:
            return []

        if not isinstance(syllables, list):
            return ["syllables must be a list."]

        if not all(isinstance(syllable, str) for syllable in syllables):
            return ["Every syllable must be a string."]

        return []