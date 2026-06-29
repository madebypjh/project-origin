import json

from research.collector import BrandCollector
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
