"""
Project Origin - Mock Report Test
"""

from .report_parser import ReportParser
from .markdown_report import MarkdownReportGenerator


def main():
    mock_response = """
{
  "executive_summary": "Project Origin은 초기 창업자가 브랜드 결정을 더 명확하게 내릴 수 있도록 돕는 AI 브랜드 전략 시스템입니다.",
  "founder_insights": "창업자는 단순한 이름 추천보다 구조화된 사고와 판단 근거를 중요하게 생각합니다.",
  "brand_identity": "AI 기반 전략적 브랜드 의사결정 도구",
  "mission_statement": "창업자가 더 나은 브랜드 결정을 내릴 수 있도록 돕는다.",
  "vision_statement": "AI 기반 브랜드 전략 컨설팅의 새로운 기준이 된다.",
  "core_values": "진실성, 품질, 구조화된 사고, 명확성",
  "positioning": "단순 네이밍 툴이 아니라 AI 브랜드 전략 컨설턴트",
  "target_audience": "브랜드 방향을 정해야 하는 초기 창업자",
  "brand_personality": "Sage + Creator",
  "naming_strategy": "신뢰, 전략, 지능, 명확성을 담은 이름을 우선한다.",
  "name_recommendations": [
    {
      "name": "OriginIQ",
      "meaning": "Origin과 Intelligence Quotient의 결합",
      "strategic_fit": "브랜드의 출발점과 지능적 판단을 함께 표현합니다.",
      "strengths": "기억하기 쉽고 AI 전략 이미지가 강합니다.",
      "weaknesses": "IQ 표현이 다소 기술 중심적으로 느껴질 수 있습니다.",
      "score": 8,
      "score_reason": "전략성과 기억성이 좋지만 감성적 깊이는 보완이 필요합니다."
    },
    {
      "name": "Brandora",
      "meaning": "Brand와 Aura의 결합",
      "strategic_fit": "브랜드의 분위기와 정체성을 강조합니다.",
      "strengths": "부드럽고 브랜드 서비스에 적합합니다.",
      "weaknesses": "AI 전략성은 상대적으로 약합니다.",
      "score": 7,
      "score_reason": "브랜드 느낌은 좋지만 차별성은 중간 수준입니다."
    }
  ],
  "final_recommendation": "OriginIQ를 1순위 후보로 추천합니다. 브랜드의 시작점과 AI 기반 전략적 판단을 동시에 담을 수 있기 때문입니다."
}
"""

    report = ReportParser.parse(mock_response)
    markdown = MarkdownReportGenerator.generate(report)

    print(markdown)


if __name__ == "__main__":
    main()