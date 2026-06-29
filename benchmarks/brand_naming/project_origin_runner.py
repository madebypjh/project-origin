"""Run benchmark cases through the deterministic Project Origin pipeline."""

import hashlib
from time import perf_counter

from benchmarks.brand_naming.models import BrandNamingBenchmarkCase
from benchmarks.brand_naming.results import BrandNamingBenchmarkOutput
from project_origin.brand.decision import NamingDecisionService
from project_origin.brand.knowledge_builder import KnowledgeBuilder
from project_origin.brand.language_engine import BrandLanguageEngine
from project_origin.brand.models import BrandLanguage, BrandKnowledge, FounderProfile
from project_origin.brand.naming.evaluator import NameEvaluator
from project_origin.brand.naming.filters import NameFilterPipeline
from project_origin.brand.naming.generation_rules import GenerationRules
from project_origin.brand.naming.generator import NamingGenerator
from project_origin.brand.naming.ranker import NameRanker
from project_origin.brand.semantic.semantic_engine import SemanticEngine


class ProjectOriginNamingRunner:
    def __init__(
        self,
        candidate_count: int = 100,
        recommendation_count: int = 5,
        seed: int = 42,
    ) -> None:
        if candidate_count < recommendation_count:
            raise ValueError(
                "candidate_count must be at least recommendation_count"
            )
        if recommendation_count <= 0:
            raise ValueError("recommendation_count must be positive")

        self.candidate_count = candidate_count
        self.recommendation_count = recommendation_count
        self.seed = seed

    def run(
        self,
        case: BrandNamingBenchmarkCase,
    ) -> BrandNamingBenchmarkOutput:
        started_at = perf_counter()
        profile = case.profile
        knowledge = KnowledgeBuilder.build(profile)
        semantic_profile = SemanticEngine.build(profile)
        brand_language = BrandLanguageEngine.build(semantic_profile)
        output = self.run_with_language(
            case=case,
            profile=profile,
            knowledge=knowledge,
            brand_language=brand_language,
            approach="project_origin",
            started_at=started_at,
        )
        return output

    def run_with_language(
        self,
        case: BrandNamingBenchmarkCase,
        profile: FounderProfile,
        knowledge: BrandKnowledge,
        brand_language: BrandLanguage,
        approach: str,
        started_at: float | None = None,
        rules: GenerationRules | None = None,
    ) -> BrandNamingBenchmarkOutput:
        started_at = perf_counter() if started_at is None else started_at
        generated = NamingGenerator.generate(
            brand_language,
            count=self.candidate_count,
            seed=self._seed_for_case(case, approach),
        )
        filtered = NameFilterPipeline.apply(generated)
        evaluated = NameEvaluator.evaluate(
            filtered,
            brand_language,
            rules=rules,
        )
        ranked = NameRanker.rank(
            evaluated,
            limit=self.recommendation_count,
        )
        decision = NamingDecisionService.decide(
            profile,
            knowledge,
            ranked,
        ).result
        selected = next(
            option.label
            for option in decision.options
            if option.identifier == decision.selected_option_id
        )
        latency_ms = round((perf_counter() - started_at) * 1000, 3)

        return BrandNamingBenchmarkOutput(
            case_id=case.identifier,
            approach=approach,
            candidates=tuple(option.label for option in decision.options),
            selected_name=selected,
            reasoning=decision.rationale,
            candidate_evaluations=tuple(
                _candidate_evaluation(candidate)
                for candidate in ranked
            ),
            latency_ms=latency_ms,
            estimated_cost_usd=0.0,
        )

    def _seed_for_case(
        self,
        case: BrandNamingBenchmarkCase,
        approach: str,
    ) -> int:
        seed_input = f"{self.seed}:{case.identifier}:{approach}"
        digest = hashlib.sha256(seed_input.encode("utf-8")).hexdigest()
        return int(digest[:8], 16)


def _candidate_evaluation(candidate) -> dict:
    return {
        "name": candidate.name,
        "total_score": candidate.total_score,
        "scores": {
            "pronunciation": candidate.pronunciation_score,
            "originality": candidate.originality_score,
            "strategic_fit": candidate.strategy_score,
            "memorability": candidate.memorability_score,
        },
        "evaluation_reason": candidate.evaluation_reason,
        "evaluation_breakdown": candidate.metadata.get(
            "evaluation_breakdown",
            {},
        ),
    }
