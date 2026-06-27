"""
Project Origin - Report Validator

Validates LLM JSON output before parsing.
"""

import json


class ReportValidator:
    REQUIRED_FIELDS = [
        "executive_summary",
        "founder_insights",
        "brand_identity",
        "mission_statement",
        "vision_statement",
        "core_values",
        "positioning",
        "target_audience",
        "brand_personality",
        "naming_strategy",
        "name_recommendations",
        "final_recommendation",
    ]

    REQUIRED_NAME_FIELDS = [
        "name",
        "meaning",
        "strategic_fit",
        "strengths",
        "weaknesses",
        "score",
        "score_reason",
    ]

    @classmethod
    def validate(cls, raw_response: str) -> dict:
        try:
            data = json.loads(raw_response)
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid JSON output: {error}") from error

        cls._validate_required_fields(data)
        cls._validate_name_recommendations(data)

        return data

    @classmethod
    def _validate_required_fields(cls, data: dict) -> None:
        missing_fields = [
            field for field in cls.REQUIRED_FIELDS
            if field not in data
        ]

        if missing_fields:
            raise ValueError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

    @classmethod
    def _validate_name_recommendations(cls, data: dict) -> None:
        recommendations = data.get("name_recommendations")

        if not isinstance(recommendations, list):
            raise ValueError("name_recommendations must be a list")

        if len(recommendations) != 5:
            raise ValueError("name_recommendations must contain exactly 5 items")

        for index, item in enumerate(recommendations, start=1):
            if not isinstance(item, dict):
                raise ValueError(
                    f"name_recommendations item {index} must be an object"
                )

            missing_fields = [
                field for field in cls.REQUIRED_NAME_FIELDS
                if field not in item
            ]

            if missing_fields:
                raise ValueError(
                    f"name_recommendations item {index} missing fields: "
                    f"{', '.join(missing_fields)}"
                )

            score = item["score"]

            if not isinstance(score, (int, float)):
                raise ValueError(
                    f"name_recommendations item {index} score must be a number"
                )

            if score < 0 or score > 10:
                raise ValueError(
                    f"name_recommendations item {index} score must be between 0 and 10"
                )