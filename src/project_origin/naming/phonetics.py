"""
Project Origin - Phonetic Rules

Provides basic pronunciation and readability checks
for generated brand name candidates.
"""


class PhoneticRules:
    VOWELS = set("aeiou")
    CONSONANTS = set("bcdfghjklmnpqrstvwxyz")

    @classmethod
    def is_pronounceable(cls, name: str) -> bool:
        normalized = name.lower().strip()

        if not normalized:
            return False

        if len(normalized) < 4 or len(normalized) > 12:
            return False

        if not normalized.isalpha():
            return False

        if not cls._has_vowel(normalized):
            return False

        if cls._has_too_many_consecutive_consonants(normalized):
            return False

        if cls._has_too_many_consecutive_vowels(normalized):
            return False

        if cls._has_repeated_characters(normalized):
            return False

        return True

    @classmethod
    def _has_vowel(cls, name: str) -> bool:
        return any(char in cls.VOWELS for char in name)

    @classmethod
    def _has_too_many_consecutive_consonants(cls, name: str) -> bool:
        count = 0

        for char in name:
            if char in cls.CONSONANTS:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 0

        return False

    @classmethod
    def _has_too_many_consecutive_vowels(cls, name: str) -> bool:
        count = 0

        for char in name:
            if char in cls.VOWELS:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 0

        return False

    @classmethod
    def _has_repeated_characters(cls, name: str) -> bool:
        for i in range(len(name) - 2):
            if name[i] == name[i + 1] == name[i + 2]:
                return True

        return False