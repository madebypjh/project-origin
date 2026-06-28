"""
Project Origin - Semantic Engine

Transforms FounderProfile into SemanticProfile.
"""

from .models import FounderProfile, SemanticProfile


class SemanticEngine:
    THEME_KEYWORDS = {
        "technology": [
            "ai", "인공지능", "automation", "자동화", "logic", "system",
            "software", "platform", "data", "intelligence", "지능",
        ],
        "trust": [
            "trust", "신뢰", "truth", "진실", "quality", "품질",
            "safe", "safety", "정확", "검증", "reliable", "reliability",
        ],
        "strategy": [
            "strategy", "전략", "decision", "의사결정", "planning",
            "framework", "structure", "구조", "reasoning", "사고", "추론",
        ],
        "premium": [
            "premium", "프리미엄", "luxury", "럭셔리", "elite",
            "고급", "quality", "품질", "refined", "sophisticated",
        ],
        "discovery": [
            "discover", "discovery", "발견", "탐색", "search",
            "reveal", "찾다", "insight", "인사이트",
        ],
        "creativity": [
            "creative", "creation", "창의", "창조", "design",
            "브랜드", "naming", "네이밍", "이름", "브랜딩",
        ],
    }

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
    }

    @classmethod
    def build(cls, profile: FounderProfile) -> SemanticProfile:
        text = cls._combine_profile_text(profile)
        themes = cls._detect_themes(text)
        dominant_theme = cls._get_dominant_theme(themes)
        vocabulary = cls._build_vocabulary(themes)
        keywords = cls._extract_keywords(text, vocabulary)

        return SemanticProfile(
            themes=themes,
            keywords=keywords,
            vocabulary=vocabulary,
            dominant_theme=dominant_theme,
        )

    @staticmethod
    def _combine_profile_text(profile: FounderProfile) -> str:
        return " ".join(
            [
                profile.problem,
                profile.audience,
                profile.vision,
                profile.principles,
                profile.differentiation,
            ]
        ).lower()

    @classmethod
    def _detect_themes(cls, text: str) -> dict[str, float]:
        raw_scores = {}

        for theme, keywords in cls.THEME_KEYWORDS.items():
            score = 0

            for keyword in keywords:
                if keyword.lower() in text:
                    score += 1

            raw_scores[theme] = score

        total_score = sum(raw_scores.values())

        if total_score == 0:
            return {
                "strategy": 0.4,
                "trust": 0.3,
                "creativity": 0.3,
            }

        return {
            theme: round(score / total_score, 2)
            for theme, score in raw_scores.items()
            if score > 0
        }

    @staticmethod
    def _get_dominant_theme(themes: dict[str, float]) -> str:
        return max(themes, key=themes.get)

    @classmethod
    def _build_vocabulary(cls, themes: dict[str, float]) -> list[str]:
        vocabulary = []

        for theme in themes:
            vocabulary.extend(cls.THEME_VOCABULARY.get(theme, []))

        return list(dict.fromkeys(vocabulary))

    @staticmethod
    def _extract_keywords(text: str, vocabulary: list[str]) -> list[str]:
        found_keywords = [
            word for word in vocabulary
            if word.lower() in text
        ]

        if found_keywords:
            return found_keywords

        return vocabulary[:8]