"""
Project Origin - Theme Detector

Detects semantic themes from founder profile text.
"""

from src.project_origin.models import FounderProfile


class ThemeDetector:
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

    @classmethod
    def detect(cls, profile: FounderProfile) -> dict[str, float]:
        text = cls._combine_profile_text(profile)
        raw_scores = cls._score_themes(text)
        return cls._normalize_scores(raw_scores)

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
    def _score_themes(cls, text: str) -> dict[str, int]:
        scores = {}

        for theme, keywords in cls.THEME_KEYWORDS.items():
            score = 0

            for keyword in keywords:
                if keyword.lower() in text:
                    score += 1

            scores[theme] = score

        return scores

    @staticmethod
    def _normalize_scores(raw_scores: dict[str, int]) -> dict[str, float]:
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