"""
Project Origin - Brand Vocabulary Builder

Builds brand language vocabulary from detected semantic themes.
"""


class VocabularyBuilder:
    THEME_VOCABULARY = {
        "technology": [
            "intelligence", "logic", "automation", "system", "signal",
            "pattern", "inference", "data", "machine", "network",
        ],
        "trust": [
            "truth", "integrity", "clarity", "confidence", "reliability",
            "transparency", "proof", "verification", "authenticity",
        ],
        "strategy": [
            "direction", "structure", "framework", "decision", "alignment",
            "focus", "priority", "positioning", "clarity", "execution",
        ],
        "premium": [
            "quality", "craft", "elegance", "prestige", "refinement",
            "timelessness", "excellence", "precision",
        ],
        "discovery": [
            "insight", "signal", "exploration", "reveal", "search",
            "origin", "path", "map", "sensemaking",
        ],
        "creativity": [
            "identity", "imagination", "creation", "expression",
            "story", "voice", "brand", "originality",
        ],
        "care": [
            "care", "balance", "rhythm", "calm", "wellbeing",
            "guidance", "privacy", "trust", "clarity",
        ],
        "industrial": [
            "material", "source", "origin", "proof", "system",
            "precision", "trace", "durability", "verification",
        ],
    }

    @classmethod
    def build(cls, themes: dict[str, float]) -> list[str]:
        vocabulary = []

        for theme in themes:
            vocabulary.extend(cls.THEME_VOCABULARY.get(theme, []))

        return list(dict.fromkeys(vocabulary))
