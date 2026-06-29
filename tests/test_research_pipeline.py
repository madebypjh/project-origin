import json

from project_origin.llm.mock_provider import MockProvider
from research.brand_list_expander import (
    BrandListExpander,
    BrandListExpansionPolicy,
)
from research.brand_list_reviewer import BrandListCandidateReviewer
from research.analyze_brand_candidates import BrandCandidateBatchAnalyzer
from research.collector import BrandCollector
from research.knowledge_compiler import KnowledgeCompiler
from research.normalizer import BrandGenomeNormalizer
from research.validator import BrandGenomeValidator


def test_collector_returns_unique_brands():
    brands = BrandCollector.get_all_brands()

    assert brands
    assert len(brands) == len(set(brands))


def test_checked_in_brand_genome_sample_is_valid():
    with open(
        "dataset/analysis/brand_genome_sample.json",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    normalized = BrandGenomeNormalizer.normalize_many(data)

    assert BrandGenomeValidator.validate_many(normalized) == []


def test_brand_genome_normalizer_handles_common_llm_variants():
    normalized = BrandGenomeNormalizer.normalize_item(
        {
            "name": "CognitiveScale",
            "industry": "AI",
            "country": "United States",
            "founded_year": 2013,
            "style": "compound",
            "name_origin": "Compound descriptive name.",
            "semantic_density": "Medium",
            "semantic_category": "intelligence",
            "brand_archetype": "Sage",
            "emotional_tone": "technical",
            "phonetic_pattern": "CVC",
            "syllables": [{"text": "Cog"}, {"text": "ni"}, {"text": "tive"}],
            "vowel_ratio": "0.4",
            "hard_consonant_ratio": "0.3",
            "soft_consonant_ratio": "0.3",
            "pronunciation_difficulty": "4",
            "memorability_score": "7",
            "distinctiveness_score": "8",
            "innovation_score": "8",
            "trust_score": "7",
            "premium_score": "6",
            "playfulness_score": "3",
            "global_scalability_score": "8",
            "morphology_type": "compound",
            "linguistic_style": "technical compound",
            "notes": "Inferred.",
        }
    )

    assert normalized["style"] == "descriptive"
    assert normalized["semantic_density"] == "medium"
    assert normalized["syllables"] == ["Cog", "ni", "tive"]
    assert BrandGenomeValidator.validate_item(normalized) == []


def test_brand_list_expansion_policy_marks_ai_output_as_candidates():
    prompt = BrandListExpansionPolicy.build_prompt(
        categories=["ai"],
        existing_brands=["OpenAI"],
        target_per_category=5,
    )

    assert "TASK: BRAND_LIST_EXPANSION_V1" in prompt
    assert "candidate brands only" in prompt
    assert "avoid brands already listed" in prompt
    assert "OpenAI" in prompt


def test_brand_list_expander_filters_existing_and_saves_candidates(tmp_path):
    expander = BrandListExpander(provider=MockProvider())

    candidates = expander.propose(categories=["ai"], target_per_category=3)
    output_path = expander.save_candidates(
        candidates,
        output_path=tmp_path / "brand_list_candidates.json",
    )
    saved = json.loads(output_path.read_text(encoding="utf-8"))

    assert candidates["ai"] == ["AiNova", "AiForge", "AiPilot"]
    assert saved["status"] == "candidate_only_requires_review"
    assert saved["categories"]["ai"] == candidates["ai"]


def test_brand_list_reviewer_promotes_only_clean_candidates(tmp_path):
    candidate_path = tmp_path / "brand_list_candidates.json"
    candidate_path.write_text(
        json.dumps(
            {
                "status": "candidate_only_requires_review",
                "categories": {
                    "ai": [
                        "OpenAI",
                        "CleanBrand",
                        "Broken챕",
                        "https://bad.example",
                    ],
                    "finance": [
                        "CleanBrand",
                        "TrustPilot",
                    ],
                },
            }
        ),
        encoding="utf-8",
    )
    output_path = tmp_path / "brand_list_reviewed.json"

    reviewed_path = BrandListCandidateReviewer().review_file(
        input_path=candidate_path,
        output_path=output_path,
    )
    reviewed = json.loads(reviewed_path.read_text(encoding="utf-8"))

    assert reviewed["status"] == "reviewed_by_rules_requires_optional_human_review"
    assert reviewed["accepted"]["ai"] == ["CleanBrand"]
    assert reviewed["accepted"]["finance"] == ["TrustPilot"]
    rejected = {
        item["name"]: item["reasons"]
        for item in reviewed["rejected"]
    }
    assert "duplicate_existing_or_cross_category" in rejected["OpenAI"]
    assert "encoding_suspect" in rejected["Broken챕"]
    assert "url_or_path" in rejected["https://bad.example"]
    assert "duplicate_existing_or_cross_category" in rejected["CleanBrand"]


def test_brand_list_reviewer_requires_candidate_status(tmp_path):
    candidate_path = tmp_path / "brand_list_candidates.json"
    candidate_path.write_text(
        json.dumps({"status": "approved", "categories": {}}),
        encoding="utf-8",
    )

    try:
        BrandListCandidateReviewer().review(candidate_path)
    except ValueError as error:
        assert "candidate_only_requires_review" in str(error)
    else:
        raise AssertionError("reviewer should reject non-candidate files")


def test_brand_candidate_batch_analyzer_creates_valid_genome_batches(tmp_path):
    reviewed_path = tmp_path / "brand_list_reviewed.json"
    reviewed_path.write_text(
        json.dumps(
            {
                "status": "reviewed_by_rules_requires_optional_human_review",
                "accepted": {
                    "ai": ["CleanBrand", "SignalMind", "ReasonLab"],
                    "finance": ["TrustPay"],
                },
                "rejected": [],
            }
        ),
        encoding="utf-8",
    )

    analyzer = BrandCandidateBatchAnalyzer(
        provider=MockProvider(),
        output_dir=tmp_path,
    )
    report = analyzer.analyze_reviewed_candidates(
        input_path=reviewed_path,
        categories=("ai",),
        batch_size=2,
        max_brands=3,
        report_path=tmp_path / "analysis_report.json",
    )

    assert report.analyzed_brand_count == 3
    assert len(report.batches) == 2
    first_batch_path = report.batches[0].output_path
    with open(first_batch_path, encoding="utf-8") as file:
        data = json.load(file)

    assert [item["name"] for item in data] == ["CleanBrand", "SignalMind"]
    assert BrandGenomeValidator.validate_many(data) == []


def test_brand_candidate_batch_analyzer_requires_reviewed_status(tmp_path):
    reviewed_path = tmp_path / "brand_list_reviewed.json"
    reviewed_path.write_text(
        json.dumps({"status": "candidate_only_requires_review", "accepted": {}}),
        encoding="utf-8",
    )
    analyzer = BrandCandidateBatchAnalyzer(
        provider=MockProvider(),
        output_dir=tmp_path,
    )

    try:
        analyzer.analyze_reviewed_candidates(input_path=reviewed_path)
    except ValueError as error:
        assert "reviewed_by_rules" in str(error)
    else:
        raise AssertionError("analyzer should reject unreviewed candidate files")


def test_knowledge_compiler_sets_usage_policy_from_sample_size():
    compiler = KnowledgeCompiler()

    reference_only = compiler._compile_group({"sample_size": 5})
    weak = compiler._compile_group({"sample_size": 15})
    soft = compiler._compile_group({"sample_size": 30})
    strong = compiler._compile_group({"sample_size": 80})

    assert reference_only["recommended_usage"] == "do_not_enforce"
    assert reference_only["knowledge_confidence"] == "insufficient"
    assert weak["recommended_usage"] == "weak_guidance"
    assert weak["knowledge_confidence"] == "low"
    assert soft["recommended_usage"] == "soft_guidance"
    assert soft["knowledge_confidence"] == "medium"
    assert strong["recommended_usage"] == "strong_guidance"
    assert strong["knowledge_confidence"] == "high"
