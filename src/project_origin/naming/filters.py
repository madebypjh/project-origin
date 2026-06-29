"""
Project Origin - Name Filters

Filters weak, duplicate, or risky generated brand name candidates.
"""

from src.project_origin.naming.phonetics import PhoneticRules


class DuplicateFilter:
    @staticmethod
    def apply(names: list[str]) -> list[str]:
        return list(dict.fromkeys(names))


class LengthFilter:
    MIN_LENGTH = 4
    MAX_LENGTH = 12

    @classmethod
    def apply(cls, names: list[str]) -> list[str]:
        return [
            name for name in names
            if cls.MIN_LENGTH <= len(name) <= cls.MAX_LENGTH
        ]


class ReservedWordFilter:
    RESERVED_WORDS = {
        "google",
        "apple",
        "microsoft",
        "amazon",
        "meta",
        "openai",
        "chatgpt",
        "facebook",
        "instagram",
        "twitter",
        "x",
        "tesla",
        "samsung",
        "naver",
        "kakao",
    }

    @classmethod
    def apply(cls, names: list[str]) -> list[str]:
        return [
            name for name in names
            if name.lower() not in cls.RESERVED_WORDS
        ]


class PronunciationFilter:
    @staticmethod
    def apply(names: list[str]) -> list[str]:
        return [
            name for name in names
            if PhoneticRules.is_pronounceable(name)
        ]


class NameFilterPipeline:
    @staticmethod
    def apply(names: list[str]) -> list[str]:
        filtered = DuplicateFilter.apply(names)
        filtered = LengthFilter.apply(filtered)
        filtered = ReservedWordFilter.apply(filtered)
        filtered = PronunciationFilter.apply(filtered)

        return filtered