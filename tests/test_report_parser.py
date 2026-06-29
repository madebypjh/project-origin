import json

from project_origin.brand.report_parser import ReportParser


def test_report_parser_creates_brand_strategy_report():
    raw_response = json.dumps(
        {
            "executive_summary": "요약",
            "founder_insights": "인사이트",
            "brand_identity": "정체성",
            "mission_statement": "미션",
            "vision_statement": "비전",
            "core_values": "가치",
            "positioning": "포지셔닝",
            "target_audience": "타깃",
            "brand_personality": "성격",
            "naming_strategy": "네이밍 전략",
            "name_recommendations": [
                {
                    "name": f"OriginIQ{i}",
                    "meaning": "의미",
                    "strategic_fit": "전략 적합성",
                    "strengths": "강점",
                    "weaknesses": "약점",
                    "score": 8,
                    "score_reason": "점수 이유",
                }
                for i in range(5)
            ],
            "final_recommendation": "최종 추천",
        },
        ensure_ascii=False,
    )

    report = ReportParser.parse(raw_response)

    assert report.executive_summary == "요약"
    assert report.name_recommendations[0].name == "OriginIQ0"
    assert len(report.name_recommendations) == 5
    assert report.final_recommendation == "최종 추천"
