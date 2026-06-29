"""
Project Origin - Brand Morphology Library

Provides brand-friendly morphemes used by the Naming Engine.
"""


class MorphologyLibrary:
    LATIN_ROOTS = [
        "ver", "nov", "via", "lum", "vita", "cura", "aura", "terra",
        "clar", "fort", "prim", "ori", "nexa", "sol", "val", "alto",
    ]

    GREEK_ROOTS = [
        "neo", "syn", "meta", "logos", "chron", "kairo", "aether",
        "phos", "dyna", "thea", "lex", "nom", "ark", "heli",
    ]

    MODERN_TECH = [
        "io", "ix", "exa", "ora", "nex", "zen", "vox", "ly", "ai",
        "byte", "logic", "mind", "core", "grid", "labs", "stack",
    ]

    PREMIUM_SOUNDS = [
        "el", "or", "ar", "ae", "ra", "on", "is", "elle", "vel",
        "luxe", "aure", "nova", "vion", "oria", "eon", "lia",
    ]

    TRUST_SOUNDS = [
        "true", "trust", "veri", "cert", "safe", "guard", "sure",
        "hon", "fide", "cred", "valid", "clear",
    ]

    STRATEGY_SOUNDS = [
        "strat", "scope", "axis", "vector", "path", "map", "signal",
        "sense", "logic", "align", "focus", "prime",
    ]

    @classmethod
    def all(cls) -> list[str]:
        return (
            cls.LATIN_ROOTS
            + cls.GREEK_ROOTS
            + cls.MODERN_TECH
            + cls.PREMIUM_SOUNDS
            + cls.TRUST_SOUNDS
            + cls.STRATEGY_SOUNDS
        )

    @classmethod
    def by_theme(cls, theme: str) -> list[str]:
        normalized_theme = theme.lower().strip()

        theme_map = {
            "latin": cls.LATIN_ROOTS,
            "greek": cls.GREEK_ROOTS,
            "tech": cls.MODERN_TECH,
            "premium": cls.PREMIUM_SOUNDS,
            "trust": cls.TRUST_SOUNDS,
            "strategy": cls.STRATEGY_SOUNDS,
        }

        return theme_map.get(normalized_theme, [])
