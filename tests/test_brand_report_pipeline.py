from project_origin.brand.markdown_report import MarkdownReportGenerator
from project_origin.brand.report_parser import ReportParser
from project_origin.llm.mock_provider import MockProvider


def test_mock_provider_output_parses_and_renders():
    raw_response = MockProvider().generate("ignored")
    report = ReportParser.parse(raw_response)
    markdown = MarkdownReportGenerator.generate(report)

    assert "# Brand Strategy Report" in markdown
    assert len(report.name_recommendations) == 5
    assert report.name_recommendations[0].name in markdown
