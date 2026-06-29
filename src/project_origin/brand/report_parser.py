"""
Project Origin - Report Parser

Parses LLM JSON output into BrandStrategyReport.
"""

from project_origin.brand.models import BrandStrategyReport, NameRecommendation
from project_origin.brand.validator import ReportValidator
from project_origin.core import DecisionResult


class ReportParser:
    @staticmethod
    def parse(
        raw_response: str,
        decision: DecisionResult | None = None,
    ) -> BrandStrategyReport:
        data = ReportValidator.validate(raw_response)
        if decision is not None:
            ReportParser._validate_decision_alignment(data, decision)

        return BrandStrategyReport(
            executive_summary=data["executive_summary"],
            founder_insights=data["founder_insights"],
            brand_identity=data["brand_identity"],
            mission_statement=data["mission_statement"],
            vision_statement=data["vision_statement"],
            core_values=data["core_values"],
            positioning=data["positioning"],
            target_audience=data["target_audience"],
            brand_personality=data["brand_personality"],
            naming_strategy=data["naming_strategy"],
            name_recommendations=[
                NameRecommendation(**item)
                for item in data["name_recommendations"]
            ],
            final_recommendation=data["final_recommendation"],
        )

    @staticmethod
    def _validate_decision_alignment(
        data: dict,
        decision: DecisionResult,
    ) -> None:
        option_names = {
            option.label.casefold(): option
            for option in decision.options
        }
        selected = next(
            option
            for option in decision.options
            if option.identifier == decision.selected_option_id
        )
        recommendation_names = {
            item["name"].casefold()
            for item in data["name_recommendations"]
        }

        unknown_names = recommendation_names - set(option_names)
        if unknown_names:
            raise ValueError(
                "Report contains names outside the DecisionResult: "
                + ", ".join(sorted(unknown_names))
            )
        if selected.label.casefold() not in recommendation_names:
            raise ValueError(
                "Report recommendations must include the selected decision option"
            )
        if selected.label.casefold() not in data["final_recommendation"].casefold():
            raise ValueError(
                "Final recommendation must preserve the selected decision option"
            )
