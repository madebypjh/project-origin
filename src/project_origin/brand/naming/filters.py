"""
Project Origin - Name Filters

Filters weak, duplicate, or risky generated brand name candidates.
"""

from project_origin.brand.naming.candidate import NameCandidate
from project_origin.brand.naming.phonetics import PhoneticRules


class DuplicateFilter:
    @staticmethod
    def apply(candidates: list[NameCandidate]) -> list[NameCandidate]:
        unique = {}
        for candidate in candidates:
            unique.setdefault(candidate.name.casefold(), candidate)
        return list(unique.values())


class LengthFilter:
    MIN_LENGTH = 4
    MAX_LENGTH = 12

    @classmethod
    def apply(cls, candidates: list[NameCandidate]) -> list[NameCandidate]:
        return [
            candidate for candidate in candidates
            if cls.MIN_LENGTH <= candidate.length <= cls.MAX_LENGTH
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
    def apply(cls, candidates: list[NameCandidate]) -> list[NameCandidate]:
        return [
            candidate for candidate in candidates
            if candidate.name.casefold() not in cls.RESERVED_WORDS
        ]


class PronunciationFilter:
    @staticmethod
    def apply(candidates: list[NameCandidate]) -> list[NameCandidate]:
        return [
            candidate for candidate in candidates
            if PhoneticRules.is_pronounceable(candidate.name)
        ]


class NameFilterPipeline:
    @staticmethod
    def apply(candidates: list[NameCandidate]) -> list[NameCandidate]:
        filtered = DuplicateFilter.apply(candidates)
        filtered = LengthFilter.apply(filtered)
        filtered = ReservedWordFilter.apply(filtered)
        filtered = PronunciationFilter.apply(filtered)

        return filtered
