import json
import pytest

from src.project_origin.validator import ReportValidator


def valid_response() -> str:
    return json.dumps(
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
                    "name": f"Name{i}",
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


def test_validator_accepts_valid_response():
    data = ReportValidator.validate(valid_response())

    assert data["executive_summary"] == "요약"
    assert len(data["name_recommendations"]) == 5


def test_validator_rejects_invalid_json():
    with pytest.raises(ValueError, match="Invalid JSON output"):
        ReportValidator.validate("{invalid json")


def test_validator_rejects_missing_required_field():
    data = json.loads(valid_response())
    del data["mission_statement"]

    with pytest.raises(ValueError, match="Missing required fields"):
        ReportValidator.validate(json.dumps(data, ensure_ascii=False))


def test_validator_rejects_wrong_recommendation_count():
    data = json.loads(valid_response())
    data["name_recommendations"] = data["name_recommendations"][:2]

    with pytest.raises(ValueError, match="exactly 5 items"):
        ReportValidator.validate(json.dumps(data, ensure_ascii=False))


def test_validator_rejects_invalid_score():
    data = json.loads(valid_response())
    data["name_recommendations"][0]["score"] = 11

    with pytest.raises(ValueError, match="between 0 and 10"):
        ReportValidator.validate(json.dumps(data, ensure_ascii=False))