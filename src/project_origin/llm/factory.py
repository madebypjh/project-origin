"""
Project Origin - LLM Provider Factory
"""

from .base import LLMProvider
from .mock_provider import MockProvider
from .openai_provider import OpenAIProvider


class LLMFactory:
    @staticmethod
    def create(provider_name: str = "mock") -> LLMProvider:
        normalized_name = provider_name.lower().strip()

        if normalized_name == "mock":
            return MockProvider()

        if normalized_name == "openai":
            return OpenAIProvider()

        raise ValueError(f"Unsupported LLM provider: {provider_name}")