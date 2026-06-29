"""
Project Origin - OpenAI Provider
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[3]
        load_dotenv(project_root / ".env")

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

        text = response.output_text.strip()

        if text.startswith("```json"):
            text = text.removeprefix("```json").strip()

        if text.startswith("```"):
            text = text.removeprefix("```").strip()

        if text.endswith("```"):
            text = text.removesuffix("```").strip()

        return text
