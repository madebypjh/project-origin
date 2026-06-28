"""
Project Origin - LLM Provider Factory

Creates LLM provider instances.
"""

from .base import LLMProvider
from .mock_provider import MockProvider


class LLMFactory:
    """
    Factory for creating LLM providers.
    """

    @staticmethod
    def create(provider_name: str = "mock") -> LLMProvider:
        """
        Create an LLM provider.

        Args:
            provider_name: Name of the provider.

        Returns:
            LLMProvider instance.
        """

        normalized_name = provider_name.lower().strip()

        if normalized_name == "mock":
            return MockProvider()

        raise ValueError(f"Unsupported LLM provider: {provider_name}")