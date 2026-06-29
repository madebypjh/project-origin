from src.project_origin.models import FounderProfile
from src.project_origin.semantic.semantic_engine import SemanticEngine
from src.project_origin.language_engine import BrandLanguageEngine


def main():
    profile = FounderProfile(
        problem="브랜드명 선택",
        audience="초기 창업자",
        vision="AI 기반 브랜드 전략 컨설팅 기업",
        principles="결과의 품질과 진실성",
        differentiation="구조화된 AI 사고력",
    )

    semantic_profile = SemanticEngine.build(profile)
    brand_language = BrandLanguageEngine.build(semantic_profile)

    print(semantic_profile.to_json())
    print()
    print(brand_language.to_json())


if __name__ == "__main__":
    main()