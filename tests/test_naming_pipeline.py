from project_origin.brand.models import BrandLanguage
from project_origin.brand.naming.candidate import NameCandidate
from project_origin.brand.naming.evaluator import NameEvaluator
from project_origin.brand.naming.filters import NameFilterPipeline
from project_origin.brand.naming.generation_rules import GenerationRulesBuilder
from project_origin.brand.naming.generator import NamingGenerator
from project_origin.brand.naming.ranker import NameRanker


def _brand_language() -> BrandLanguage:
    return BrandLanguage(
        vocabulary=["intelligence", "trust", "strategy"],
        tone="credible",
        emotion="confidence",
        style="modern",
        semantic_direction="Trustworthy decision intelligence",
    )


def test_generator_is_reproducible_and_returns_structured_candidates():
    first = NamingGenerator.generate(_brand_language(), count=10, seed=7)
    second = NamingGenerator.generate(_brand_language(), count=10, seed=7)

    assert [candidate.name for candidate in first] == [
        candidate.name for candidate in second
    ]
    assert all(isinstance(candidate, NameCandidate) for candidate in first)
    assert all(
        "generation_pattern" in candidate.metadata for candidate in first
    )
    assert all(
        "generation_signature" in candidate.metadata for candidate in first
    )


def test_generator_uses_multiple_generation_patterns():
    generated = NamingGenerator.generate(_brand_language(), count=40, seed=11)
    patterns = {
        candidate.metadata["generation_pattern"]
        for candidate in generated
    }

    assert len(patterns) >= 3


def test_generator_can_use_intuitive_and_literal_terms_when_intent_supports_it():
    brand_language = BrandLanguage(
        vocabulary=["ai", "data", "system"],
        tone="technical",
        emotion="confidence",
        style="modern",
        semantic_direction="AI data platform for developer workflow",
    )
    generated = NamingGenerator.generate(brand_language, count=80, seed=19)
    generated_roots = {
        root
        for candidate in generated
        for root in candidate.metadata["generation_roots"]
    }

    assert generated_roots & {"ai", "data", "clou", "stac", "labs"}


def test_ranker_prefers_distinct_generation_signatures():
    candidates = [
        NameCandidate(
            name="Oripath",
            total_score=9.0,
            metadata={"generation_signature": "ori:path"},
        ),
        NameCandidate(
            name="Pathori",
            total_score=8.9,
            metadata={"generation_signature": "ori:path"},
        ),
        NameCandidate(
            name="Tracecore",
            total_score=8.5,
            metadata={"generation_signature": "core:trace"},
        ),
    ]

    ranked = NameRanker.rank(candidates, limit=2)

    assert [candidate.name for candidate in ranked] == [
        "Oripath",
        "Tracecore",
    ]


def test_filter_and_evaluator_keep_candidate_objects():
    candidates = [
        NameCandidate(name="Validora"),
        NameCandidate(name="validora"),
        NameCandidate(name="OpenAI"),
        NameCandidate(name="bcdf"),
    ]

    filtered = NameFilterPipeline.apply(candidates)
    evaluated = NameEvaluator.evaluate(filtered, _brand_language())

    assert [candidate.name for candidate in filtered] == ["Validora"]
    assert evaluated[0].name == "Validora"
    assert evaluated[0].total_score > 0
    assert (
        evaluated[0].metadata["evaluation_breakdown"]["version"]
        == "brand_naming_evaluation_v1"
    )
    assert "strategic_fit" in (
        evaluated[0].metadata["evaluation_breakdown"]["components"]
    )


def test_generation_rules_builder_marks_small_sample_as_weak_guidance():
    rules = GenerationRulesBuilder.build(
        {
            "sample_size": 15,
            "recommended_name_length": 7,
            "recommended_syllable_count": 2,
            "recommended_vowel_ratio": 0.42,
            "recommended_hard_consonant_ratio": 0.38,
            "recommended_soft_consonant_ratio": 0.20,
        }
    )

    assert rules.knowledge_confidence == "low"
    assert rules.recommended_usage == "weak_guidance"
    assert rules.guidance_strength == 0.05


def test_evaluator_can_apply_naming_knowledge_as_soft_guidance():
    candidate = NameCandidate(name="Strategia")
    rules = GenerationRulesBuilder.build(
        {
            "sample_size": 15,
            "recommended_name_length": 9,
            "recommended_vowel_ratio": 0.4,
            "recommended_hard_consonant_ratio": 0.25,
            "recommended_soft_consonant_ratio": 0.35,
        }
    )

    without_rules = NameEvaluator.evaluate([candidate], _brand_language())[0]
    with_rules = NameEvaluator.evaluate(
        [candidate],
        _brand_language(),
        rules=rules,
    )[0]

    assert "Naming knowledge contributed weakly" not in (
        without_rules.evaluation_reason or ""
    )
    assert "Naming knowledge contributed weakly" in (
        with_rules.evaluation_reason or ""
    )
    assert (
        with_rules.metadata["evaluation_breakdown"]["knowledge_guidance"][
            "applied"
        ]
        is True
    )


def test_evaluator_prioritizes_strategic_fit_in_final_score():
    brand_language = BrandLanguage(
        vocabulary=["trust", "logic", "clarity"],
        tone="credible",
        emotion="confidence",
        style="modern",
        semantic_direction="Trustworthy logic and clarity",
    )
    evaluated = NameEvaluator.evaluate(
        [
            NameCandidate(name="Trustlogic"),
            NameCandidate(name="Voxaluma"),
        ],
        brand_language,
    )
    by_name = {candidate.name: candidate for candidate in evaluated}
    strong_fit = by_name["Trustlogic"]
    weak_fit = by_name["Voxaluma"]

    assert strong_fit.strategy_score > weak_fit.strategy_score
    assert strong_fit.total_score > weak_fit.total_score
    assert (
        strong_fit.metadata["evaluation_breakdown"]["components"][
            "strategic_fit"
        ]["weight"]
        == 0.65
    )
