"""
Project Origin - LLM Base Interface

Defines the provider-independent interface for all LLM providers.
"""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Base interface for all LLM providers.

    Every provider must implement generate().
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response from the LLM provider.

        Args:
            prompt: The complete prompt string.

        Returns:
            Raw text response from the provider.
        """
        raise NotImplementedError