from project_origin.brand.models import BrandLanguage
from project_origin.brand.naming.candidate import NameCandidate
from project_origin.brand.naming.evaluator import NameEvaluator
from project_origin.brand.naming.filters import NameFilterPipeline
from project_origin.brand.naming.generator import NamingGenerator


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
