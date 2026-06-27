"""
Project Origin - Markdown Report Generator
"""

from .models import BrandStrategyReport


class MarkdownReportGenerator:
    @staticmethod
    def generate(report: BrandStrategyReport) -> str:
        names = ""

        for item in report.name_recommendations:
            names += f"""
### {item["name"]}

- **Meaning:** {item["meaning"]}
- **Strategic Fit:** {item["strategic_fit"]}
- **Strengths:** {item["strengths"]}
- **Weaknesses:** {item["weaknesses"]}
- **Score:** {item["score"]}/10
- **Reason:** {item["score_reason"]}
"""

        return f"""# Brand Strategy Report

## Executive Summary

{report.executive_summary}

## Founder Insights

{report.founder_insights}

## Brand Identity

{report.brand_identity}

## Mission Statement

{report.mission_statement}

## Vision Statement

{report.vision_statement}

## Core Values

{report.core_values}

## Positioning

{report.positioning}

## Target Audience

{report.target_audience}

## Brand Personality

{report.brand_personality}

## Naming Strategy

{report.naming_strategy}

## Name Recommendations

{names}

## Final Recommendation

{report.final_recommendation}
"""