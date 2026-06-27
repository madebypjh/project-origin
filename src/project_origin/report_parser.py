"""
Project Origin - Report Parser

Parses LLM JSON output into BrandStrategyReport.
"""

import json

from .models import BrandStrategyReport
from .validator import ReportValidator


class ReportParser:
    @staticmethod
    def parse(raw_response: str) -> BrandStrategyReport:
        data = ReportValidator.validate(raw_response)

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
            name_recommendations=data["name_recommendations"],
            final_recommendation=data["final_recommendation"],
        )