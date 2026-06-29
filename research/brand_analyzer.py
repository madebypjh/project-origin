"""
Project Origin - Brand Analyzer

Analyzes famous brand names using OpenAI and produces Brand Genome JSON.
"""

import json
from pathlib import Path

from project_origin.llm.base import LLMProvider
from project_origin.llm.openai_provider import OpenAIProvider
from research.normalizer import BrandGenomeNormalizer
from research.validator import BrandGenomeValidator


class BrandAnalyzer:
    def __init__(
        self,
        provider: LLMProvider | None = None,
        output_dir: Path | None = None,
    ) -> None:
        project_root = Path(__file__).resolve().parents[1]

        self.project_root = project_root
        self.prompt_path = project_root / "research" / "prompts" / "brand_analysis_prompt.md"
        self.output_dir = output_dir or project_root / "dataset" / "analysis"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.provider = provider or OpenAIProvider()

    def analyze(self, brands: list[str], filename: str = "brand_genome_sample.json") -> Path:
        prompt_template = self.prompt_path.read_text(encoding="utf-8")
        brand_list = "\n".join([f"- {brand}" for brand in brands])
        prompt = prompt_template.replace("{{BRAND_LIST}}", brand_list)

        raw_text = self._clean_json_response(self.provider.generate(prompt))

        data = json.loads(raw_text)
        data = BrandGenomeNormalizer.normalize_many(data)

        errors = BrandGenomeValidator.validate_many(data)

        if errors:
            error_messages = []

            for item in errors:
                error_messages.append(
                    f"{item['name']} -> {', '.join(item['errors'])}"
                )

            raise ValueError(
                "Brand Genome validation failed:\n\n"
                + "\n".join(error_messages)
            )

        output_path = self.output_dir / filename

        output_path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return output_path

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
    brands = [
        "Google",
        "Spotify",
        "Kodak",
        "Rolex",
        "Nvidia",
    ]

    analyzer = BrandAnalyzer()
    output_path = analyzer.analyze(brands)

    print(f"Brand genome saved to: {output_path}")


if __name__ == "__main__":
    main()
