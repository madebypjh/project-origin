"""
Project Origin - Markdown Report Generator
"""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from project_origin.brand.models import BrandStrategyReport


class MarkdownReportGenerator:
    @staticmethod
    def generate(report: BrandStrategyReport) -> str:
        project_root = Path(__file__).resolve().parents[3]
        template_dir = project_root / "templates"

        env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        template = env.get_template("brand_report.md")

        return template.render(report=report)
