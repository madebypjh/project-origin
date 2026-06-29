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

    CREATIVITY_SOUNDS = [
        "vox", "muse", "narr", "lyra", "folio", "verse", "luma",
        "aria", "echo", "nova",
    ]

    DISCOVERY_SOUNDS = [
        "ori", "trace", "nexa", "path", "terra", "cycle", "source",
        "prove", "root", "via",
    ]

    CARE_SOUNDS = [
        "cura", "vita", "aura", "calm", "luma", "mira", "vela",
        "rhythm", "bal", "kind",
    ]

    INDUSTRIAL_SOUNDS = [
        "forge", "axis", "grid", "core", "trace", "terra", "steel",
        "source", "vector", "cert",
    ]

    EDUCATION_SOUNDS = [
        "learn", "luma", "step", "path", "mira", "nurt", "grow",
        "vela", "kind", "clar",
    ]

    LEGAL_SOUNDS = [
        "lex", "claus", "fide", "cert", "veri", "plain", "caut",
        "bound", "true", "valid",
    ]

    CLIMATE_SOUNDS = [
        "terra", "resil", "clima", "asset", "aqua", "adapt", "ori",
        "trace", "nexa", "field",
    ]

    PRIVACY_SOUNDS = [
        "priv", "consent", "local", "safe", "veil", "aura", "trust",
        "clear", "guard", "kind",
    ]

    LOGISTICS_SOUNDS = [
        "route", "flow", "relay", "grid", "signal", "path", "vector",
        "scope", "axis",
    ]

    ROBOTICS_SOUNDS = [
        "robo", "fleet", "forge", "axis", "oper", "safe", "signal",
        "grid", "mech", "core",
    ]

    WELLNESS_SOUNDS = [
        "calm", "mira", "aura", "vela", "kind", "reflect", "luma",
        "bal", "gent", "cura",
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
            + cls.CREATIVITY_SOUNDS
            + cls.DISCOVERY_SOUNDS
            + cls.CARE_SOUNDS
            + cls.INDUSTRIAL_SOUNDS
            + cls.EDUCATION_SOUNDS
            + cls.LEGAL_SOUNDS
            + cls.CLIMATE_SOUNDS
            + cls.PRIVACY_SOUNDS
            + cls.LOGISTICS_SOUNDS
            + cls.ROBOTICS_SOUNDS
            + cls.WELLNESS_SOUNDS
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
            "creativity": cls.CREATIVITY_SOUNDS,
            "discovery": cls.DISCOVERY_SOUNDS,
            "care": cls.CARE_SOUNDS,
            "industrial": cls.INDUSTRIAL_SOUNDS,
            "education": cls.EDUCATION_SOUNDS,
            "legal": cls.LEGAL_SOUNDS,
            "climate": cls.CLIMATE_SOUNDS,
            "privacy": cls.PRIVACY_SOUNDS,
            "logistics": cls.LOGISTICS_SOUNDS,
            "robotics": cls.ROBOTICS_SOUNDS,
            "wellness": cls.WELLNESS_SOUNDS,
        }

        return theme_map.get(normalized_theme, [])
