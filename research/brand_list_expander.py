"""AI-assisted expansion of Brand Genome research brand lists.

The expander proposes candidates only. Proposed brands must be reviewed before
they are promoted into the curated BrandCollector lists or Brand Genome data.
"""

from __future__ import annotations

import json
from pathlib import Path

from project_origin.llm.base import LLMProvider
from project_origin.llm.openai_provider import OpenAIProvider
from research.collector import BrandCollector


class BrandListExpansionPolicy:
    VERSION = "brand_list_expansion_v1"

    @classmethod
    def build_prompt(
        cls,
        categories: list[str],
        existing_brands: list[str],
        target_per_category: int,
    ) -> str:
        categories_json = json.dumps(categories, ensure_ascii=False, indent=2)
        existing_json = json.dumps(existing_brands, ensure_ascii=False, indent=2)
        return f"""
TASK: BRAND_LIST_EXPANSION_V1
POLICY_VERSION: {cls.VERSION}

You are proposing candidate brand names for Project Origin's Brand Genome
research dataset.

Important:
- Return candidate brands only; do not analyze the brands.
- Prefer commercially recognized companies or products with distinctive names.
- Do not include people, generic categories, taglines, or URLs.
- Avoid duplicates and avoid brands already listed in EXISTING_BRANDS.
- Use common public-facing brand names, not legal entity names.
- Include a mix of established and modern brands where possible.
- These are research candidates; do not claim the list is complete.

Return ONLY valid JSON with this shape:

{{
  "categories": [
    {{
      "category": "",
      "brands": [""]
    }}
  ]
}}

TARGET_PER_CATEGORY: {target_per_category}

CATEGORIES:
{categories_json}

EXISTING_BRANDS:
{existing_json}
""".strip()


class BrandListExpander:
    DEFAULT_OUTPUT_PATH = (
        Path("dataset") / "analysis" / "brand_list_candidates.json"
    )

    def __init__(self, provider: LLMProvider | None = None) -> None:
        self.project_root = Path(__file__).resolve().parents[1]
        self.provider = provider or OpenAIProvider()

    def propose(
        self,
        categories: list[str] | None = None,
        target_per_category: int = 30,
    ) -> dict[str, list[str]]:
        if target_per_category <= 0:
            raise ValueError("target_per_category must be positive")

        categories = categories or BrandCollector.get_categories()
        if not categories:
            raise ValueError("categories must not be empty")

        prompt = BrandListExpansionPolicy.build_prompt(
            categories=categories,
            existing_brands=BrandCollector.get_all_brands(),
            target_per_category=target_per_category,
        )
        raw_response = self.provider.generate(prompt)
        return self._parse_response(raw_response, categories)

    def save_candidates(
        self,
        candidates: dict[str, list[str]],
        output_path: Path | None = None,
    ) -> Path:
        requested_path = output_path or self.DEFAULT_OUTPUT_PATH
        path = (
            requested_path
            if requested_path.is_absolute()
            else self.project_root / requested_path
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "status": "candidate_only_requires_review",
                    "policy_version": BrandListExpansionPolicy.VERSION,
                    "categories": candidates,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        return path

    def _parse_response(
        self,
        raw_response: str,
        requested_categories: list[str],
    ) -> dict[str, list[str]]:
        data = json.loads(self._clean_json_response(raw_response))
        if not isinstance(data, dict):
            raise ValueError("Brand list expansion response must be an object")
        raw_categories = data.get("categories")
        if not isinstance(raw_categories, list):
            raise ValueError("Brand list expansion categories must be a list")

        requested = {
            category.casefold().strip(): category
            for category in requested_categories
        }
        existing = {
            brand.casefold().strip()
            for brand in BrandCollector.get_all_brands()
        }
        candidates: dict[str, list[str]] = {
            category: [] for category in requested_categories
        }

        for item in raw_categories:
            if not isinstance(item, dict):
                raise ValueError("Every category proposal must be an object")
            category = str(item.get("category", "")).strip()
            normalized_category = category.casefold()
            if normalized_category not in requested:
                continue
            brands = item.get("brands")
            if not isinstance(brands, list):
                raise ValueError("Category proposal brands must be a list")

            target_category = requested[normalized_category]
            for brand in brands:
                cleaned = self._clean_brand_name(brand)
                if not cleaned:
                    continue
                normalized_brand = cleaned.casefold()
                if normalized_brand in existing:
                    continue
                if normalized_brand in {
                    existing_brand.casefold()
                    for existing_brand in candidates[target_category]
                }:
                    continue
                candidates[target_category].append(cleaned)

        return candidates

    @staticmethod
    def _clean_brand_name(value) -> str:
        if not isinstance(value, str):
            return ""
        cleaned = " ".join(value.strip().split())
        if not cleaned:
            return ""
        if "://" in cleaned or "/" in cleaned:
            return ""
        if len(cleaned) > 40:
            return ""
        return cleaned

    @staticmethod
    def _clean_json_response(text: str) -> str:
        cleaned = text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned.removeprefix("```json").strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.removeprefix("```").strip()
        if cleaned.endswith("```"):
            cleaned = cleaned.removesuffix("```").strip()
        return cleaned


def main() -> None:
    expander = BrandListExpander()
    candidates = expander.propose()
    output_path = expander.save_candidates(candidates)
    print(f"Brand list candidates saved to: {output_path}")


if __name__ == "__main__":
    main()
