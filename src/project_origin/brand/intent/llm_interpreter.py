"""LLM-assisted Brand intent interpretation with strict Core validation."""

import json

from project_origin.brand.intent.adapter import BrandIntentAdapter
from project_origin.brand.intent.policy import BrandIntentPolicy
from project_origin.brand.models import FounderProfile
from project_origin.core import (
    IntentNormalizer,
    IntentProfile,
    IntentSignal,
    IntentValidator,
)
from project_origin.llm.base import LLMProvider


class LlmBrandIntentInterpreter:
    MAX_SIGNALS = 12

    def __init__(self, provider: LLMProvider) -> None:
        self.provider = provider

    def interpret(self, input_data: FounderProfile) -> IntentProfile:
        prompt = BrandIntentPolicy.build_prompt(input_data)
        raw_response = self.provider.generate(prompt)
        data = self._parse_response(raw_response)
        raw_signals = data["signals"]

        if not raw_signals:
            raise ValueError("LLM intent response must contain at least one signal")
        if len(raw_signals) > self.MAX_SIGNALS:
            raise ValueError(
                f"LLM intent response exceeds {self.MAX_SIGNALS} signals"
            )

        signals = IntentNormalizer.normalize(
            self._build_signal(item)
            for item in raw_signals
        )
        unresolved = self._parse_unresolved(data.get("unresolved_signals", []))
        profile = BrandIntentAdapter.to_intent_profile(
            input_data,
            signals=signals,
            unresolved_signals=unresolved,
        )
        return IntentValidator.validate(
            profile,
            BrandIntentAdapter.source_text(input_data),
        )

    @staticmethod
    def _parse_response(raw_response: str) -> dict:
        try:
            data = json.loads(raw_response)
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid intent JSON output: {error}") from error

        if not isinstance(data, dict):
            raise ValueError("LLM intent response must be a JSON object")
        if not isinstance(data.get("signals"), list):
            raise ValueError("LLM intent response signals must be a list")
        return data

    @staticmethod
    def _build_signal(item: dict) -> IntentSignal:
        if not isinstance(item, dict):
            raise ValueError("Every LLM intent signal must be an object")

        required = {"kind", "concept", "weight", "evidence", "confidence"}
        missing = sorted(required - set(item))
        if missing:
            raise ValueError(
                f"LLM intent signal missing fields: {', '.join(missing)}"
            )
        evidence = item["evidence"]
        if not isinstance(evidence, list) or not all(
            isinstance(value, str)
            for value in evidence
        ):
            raise ValueError("LLM intent signal evidence must be a string list")
        for field_name in ("weight", "confidence"):
            value = item[field_name]
            if (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
            ):
                raise ValueError(
                    f"LLM intent signal {field_name} must be a number"
                )

        return IntentSignal(
            kind=str(item["kind"]),
            concept=str(item["concept"]),
            weight=item["weight"],
            evidence=tuple(evidence),
            confidence=item["confidence"],
            metadata={"source": "llm"},
        )

    @staticmethod
    def _parse_unresolved(value) -> tuple[str, ...]:
        if not isinstance(value, list) or not all(
            isinstance(item, str) and item.strip()
            for item in value
        ):
            raise ValueError("unresolved_signals must be a string list")
        return tuple(item.strip() for item in value)
