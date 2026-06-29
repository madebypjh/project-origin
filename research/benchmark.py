"""
Project Origin - Naming Benchmark

Benchmarks Naming Engine output quality.
"""

from statistics import mean

from src.project_origin.models import FounderProfile
from src.project_origin.semantic.semantic_engine import SemanticEngine
from src.project_origin.language_engine import BrandLanguageEngine
from src.project_origin.naming.generator import NamingGenerator
from src.project_origin.naming.filters import NameFilterPipeline
from src.project_origin.naming.evaluator import NameEvaluator
from src.project_origin.naming.ranker import NameRanker


class NamingBenchmark:
    @staticmethod
    def run() -> None:
        profile = FounderProfile(
            problem="브랜드명 만들기",
            audience="버그헌터와 보안업체",
            vision="세계적인 보안 프로그램 업체",
            principles="결과의 품질",
            differentiation="AI 프롬프트 엔진 기반의 고도화된 사고력",
        )

        semantic_profile = SemanticEngine.build(profile)
        brand_language = BrandLanguageEngine.build(semantic_profile)

        generated_names = NamingGenerator.generate(brand_language, count=300)
        filtered_names = NameFilterPipeline.apply(generated_names)
        evaluated_names = NameEvaluator.evaluate(filtered_names, brand_language)
        ranked_names = NameRanker.rank(evaluated_names, limit=20)

        NamingBenchmark._print_report(
            generated_names=generated_names,
            filtered_names=filtered_names,
            ranked_names=ranked_names,
        )

    @staticmethod
    def _print_report(
        generated_names,
        filtered_names,
        ranked_names,
    ) -> None:
        duplicate_rate = 1 - (len(set(generated_names)) / len(generated_names))

        print("\n===== NAMING ENGINE BENCHMARK =====\n")

        print(f"Generated Names: {len(generated_names)}")
        print(f"Filtered Names: {len(filtered_names)}")
        print(f"Top Ranked Names: {len(ranked_names)}")
        print(f"Duplicate Rate: {duplicate_rate:.2%}")

        if ranked_names:
            print(f"Average Total Score: {mean([n.total_score for n in ranked_names]):.2f}")
            print(f"Average Pronunciation: {mean([n.pronunciation_score for n in ranked_names]):.2f}")
            print(f"Average Originality: {mean([n.originality_score for n in ranked_names]):.2f}")
            print(f"Average Strategy Fit: {mean([n.strategy_score for n in ranked_names]):.2f}")
            print(f"Average Memorability: {mean([n.memorability_score for n in ranked_names]):.2f}")

        print("\n===== TOP 20 =====\n")

        for index, name in enumerate(ranked_names, start=1):
            print(f"{index}. {name.name} — {name.total_score}/10")


def main() -> None:
    NamingBenchmark.run()


if __name__ == "__main__":
    main()