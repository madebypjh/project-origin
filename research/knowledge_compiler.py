"""
Project Origin - Knowledge Compiler

Compiles extracted brand patterns into generator-friendly naming knowledge.
"""

import json
from pathlib import Path


class KnowledgeCompiler:
    def __init__(self) -> None:
        self.project_root = Path(__file__).resolve().parents[1]
        self.patterns_path = (
            self.project_root
            / "dataset"
            / "analysis"
            / "brand_patterns.json"
        )
        self.output_path = (
            self.project_root
            / "dataset"
            / "analysis"
            / "naming_knowledge.json"
        )

    def compile(self) -> Path:
        patterns = self._load_patterns()

        knowledge = {
            "global": self._compile_group(patterns.get("global", {})),
            "by_industry": {
                industry: self._compile_group(group_patterns)
                for industry, group_patterns in patterns.get("by_industry", {}).items()
            },
        }

        self.output_path.write_text(
            json.dumps(knowledge, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return self.output_path

    def _load_patterns(self) -> dict:
        if not self.patterns_path.exists():
            raise FileNotFoundError(
                "dataset/analysis/brand_patterns.json not found. "
                "Run: python -m research.pattern_extractor"
            )

        return json.loads(self.patterns_path.read_text(encoding="utf-8"))

    def _compile_group(self, patterns: dict) -> dict:
        if not patterns:
            return {}

        sample_size = int(patterns.get("sample_size", 0) or 0)
        dominant_style = patterns.get("dominant_style", "unknown")
        dominant_tone = patterns.get("dominant_emotional_tone", "unknown")
        dominant_archetype = patterns.get("dominant_archetype", "unknown")

        style_distribution = patterns.get("style_distribution", {})
        tone_distribution = patterns.get("emotional_tone_distribution", {})

        return {
            "sample_size": sample_size,
            "knowledge_confidence": self._sample_confidence(sample_size),
            "recommended_usage": self._recommended_usage(sample_size),
            "usage_rationale": self._usage_rationale(sample_size),
            "preferred_style": dominant_style,
            "preferred_style_confidence": self._confidence(
                style_distribution.get(dominant_style, 0)
            ),
            "preferred_tone": dominant_tone,
            "preferred_tone_confidence": self._confidence(
                tone_distribution.get(dominant_tone, 0)
            ),
            "preferred_archetype": dominant_archetype,
            "recommended_name_length": round(
                patterns.get("average_name_length", 0)
            ),
            "recommended_syllable_count": round(
                patterns.get("average_syllable_count", 0)
            ),
            "recommended_vowel_ratio": patterns.get("average_vowel_ratio", 0),
            "recommended_hard_consonant_ratio": patterns.get(
                "average_hard_consonant_ratio",
                0,
            ),
            "recommended_soft_consonant_ratio": patterns.get(
                "average_soft_consonant_ratio",
                0,
            ),
            "recommended_scores": patterns.get("average_scores", {}),
            "generator_guidance": self._build_guidance(patterns),
        }

    @staticmethod
    def _confidence(value: float) -> str:
        if value >= 0.7:
            return "high"

        if value >= 0.4:
            return "medium"

        if value > 0:
            return "low"

        return "unknown"

    @staticmethod
    def _sample_confidence(sample_size: int) -> str:
        if sample_size >= 80:
            return "high"

        if sample_size >= 30:
            return "medium"

        if sample_size >= 10:
            return "low"

        return "insufficient"

    @staticmethod
    def _recommended_usage(sample_size: int) -> str:
        if sample_size >= 80:
            return "strong_guidance"

        if sample_size >= 30:
            return "soft_guidance"

        if sample_size >= 10:
            return "weak_guidance"

        return "do_not_enforce"

    @staticmethod
    def _usage_rationale(sample_size: int) -> str:
        if sample_size >= 80:
            return (
                "The pattern sample is large enough to influence ranking, "
                "while still remaining subordinate to strategy fit."
            )

        if sample_size >= 30:
            return (
                "The pattern sample is useful as soft ranking guidance, "
                "but should not override case-specific brand strategy."
            )

        if sample_size >= 10:
            return (
                "The pattern sample is early-stage evidence. Use only as weak "
                "guidance during comparison, not as a hard rule."
            )

        return (
            "The pattern sample is too small to influence generated names. "
            "Keep it for reference only."
        )

    def _build_guidance(self, patterns: dict) -> list[str]:
        guidance = []

        style = patterns.get("dominant_style")
        tone = patterns.get("dominant_emotional_tone")
        average_length = patterns.get("average_name_length", 0)
        average_syllables = patterns.get("average_syllable_count", 0)
        hard_ratio = patterns.get("average_hard_consonant_ratio", 0)
        soft_ratio = patterns.get("average_soft_consonant_ratio", 0)

        if style and style != "unknown":
            guidance.append(f"Prefer {style} naming style.")

        if tone and tone != "unknown":
            guidance.append(f"Express a {tone} emotional tone.")

        if average_length:
            guidance.append(
                f"Target names around {round(average_length)} characters."
            )

        if average_syllables:
            guidance.append(
                f"Target around {round(average_syllables)} syllables."
            )

        if hard_ratio >= 0.4:
            guidance.append("Use stronger consonants for impact.")

        if soft_ratio >= 0.4:
            guidance.append("Use softer consonants for approachability.")

        return guidance


def main() -> None:
    compiler = KnowledgeCompiler()
    output_path = compiler.compile()

    print(f"Naming knowledge compiled: {output_path}")


if __name__ == "__main__":
    main()
