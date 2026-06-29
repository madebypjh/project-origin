from project_origin.brand.models import FounderProfile, SemanticProfile
from project_origin.brand.semantic.semantic_engine import SemanticEngine


def test_semantic_engine_creates_semantic_profile():
    profile = FounderProfile(
        problem="브랜드명 선택",
        audience="초기 창업자",
        vision="AI 기반 브랜드 전략 컨설팅 기업",
        principles="결과의 품질과 진실성",
        differentiation="구조화된 AI 사고력",
    )

    semantic_profile = SemanticEngine.build(profile)

    assert isinstance(semantic_profile, SemanticProfile)
    assert semantic_profile.dominant_theme in semantic_profile.themes
    assert len(semantic_profile.vocabulary) > 0
    assert len(semantic_profile.keywords) > 0


def test_semantic_engine_detects_relevant_themes():
    profile = FounderProfile(
        problem="AI 기반 의사결정 지원",
        audience="초기 창업자",
        vision="전략적 판단을 돕는 플랫폼",
        principles="신뢰와 품질",
        differentiation="구조화된 추론",
    )

    semantic_profile = SemanticEngine.build(profile)

    assert "technology" in semantic_profile.themes
    assert "trust" in semantic_profile.themes
    assert "strategy" in semantic_profile.themes


def test_semantic_engine_uses_fallback_when_no_theme_detected():
    profile = FounderProfile(
        problem="테스트",
        audience="테스트",
        vision="테스트",
        principles="테스트",
        differentiation="테스트",
    )

    semantic_profile = SemanticEngine.build(profile)

    assert semantic_profile.themes == {
        "strategy": 0.4,
        "trust": 0.3,
        "creativity": 0.3,
    }
    assert semantic_profile.dominant_theme == "strategy"
