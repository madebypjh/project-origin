from src.project_origin.models import FounderProfile
from src.project_origin.semantic.semantic_engine import SemanticEngine
from src.project_origin.language_engine import BrandLanguageEngine
from src.project_origin.naming.generator import NamingGenerator
from src.project_origin.naming.evaluator import NameEvaluator
from src.project_origin.naming.ranker import NameRanker


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

    names = NamingGenerator.generate(brand_language, count=100)
    evaluated_names = NameEvaluator.evaluate(names, brand_language)
    ranked_names = NameRanker.rank(evaluated_names, limit=20)

    print("\n===== SEMANTIC PROFILE =====\n")
    print(semantic_profile.to_json())

    print("\n===== BRAND LANGUAGE =====\n")
    print(brand_language.to_json())

    print("\n===== TOP RANKED NAMES =====\n")

    for index, candidate in enumerate(ranked_names, start=1):
        print(f"{index}. {candidate.name}")
        print(f"   Total Score: {candidate.total_score}/10")
        print(f"   Pronunciation: {candidate.pronunciation_score}/10")
        print(f"   Originality: {candidate.originality_score}/10")
        print(f"   Strategy Fit: {candidate.strategy_score}/10")
        print(f"   Memorability: {candidate.memorability_score}/10")
        print(f"   Reason: {candidate.evaluation_reason}")
        print()


if __name__ == "__main__":
    main()