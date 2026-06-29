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
        "education": [
            "learn", "guide", "step", "growth", "agency",
            "progress", "confidence", "path",
        ],
        "legal": [
            "clause", "review", "caution", "clarity", "boundary",
            "risk", "plain", "trust",
        ],
        "climate": [
            "climate", "resilience", "scenario", "asset", "adapt",
            "risk", "evidence", "planning",
        ],
        "privacy": [
            "privacy", "consent", "control", "local", "agency",
            "personal", "safe", "trust",
        ],
        "logistics": [
            "route", "flow", "signal", "shipment", "escalation",
            "visibility", "priority", "dependability",
        ],
        "robotics": [
            "robot", "fleet", "operator", "safety", "signal",
            "control", "warehouse", "coordination",
        ],
        "wellness": [
            "calm", "reflect", "gentle", "support", "privacy",
            "boundary", "care", "balance",
        ],
    }

    @classmethod
    def build(cls, themes: dict[str, float]) -> list[str]:
        vocabulary = []

        for theme in themes:
            vocabulary.extend(cls.THEME_VOCABULARY.get(theme, []))

        return list(dict.fromkeys(vocabulary))
