"""
Project Origin - OpenAI Provider
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self) -> None:
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in .env")

        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response.output_text