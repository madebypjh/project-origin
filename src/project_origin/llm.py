"""
Project Origin - LLM Client

Provider-independent LLM interface.
"""

import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from openai import OpenAI


class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class OpenAIClient(LLMClient):
    def __init__(self, model: str = "gpt-4.1-mini"):
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in .env")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response.output_text