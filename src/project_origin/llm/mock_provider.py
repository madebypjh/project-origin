"""
Project Origin - Mock LLM Provider

Provides a deterministic mock response for development and testing.
"""

import json
import re

from .base import LLMProvider


class MockProvider(LLMProvider):
    """
    Mock implementation of the LLM provider.

    Used during development before integrating a real LLM.
    """

    def generate(self, prompt: str) -> str:
        """
        Ignore the prompt and return a fixed mock response.

        Args:
            prompt: Complete prompt string.

        Returns:
            JSON string representing a brand strategy report.
        """

        if "TASK: INTENT_INTERPRETATION_V1" in prompt:
            return self._generate_intent_response(prompt)

        selected_name, candidate_names = self._extract_decision(prompt)

        report = {
            "executive_summary": (
                "Project Origin은 초기 창업자가 더 나은 브랜드 의사결정을 "
                "내릴 수 있도록 돕는 AI 브랜드 전략 플랫폼입니다."
            ),
            "founder_insights": (
                "창업자는 단순한 네이밍보다 구조화된 사고와 "
                "전략적 근거를 중요하게 생각합니다."
            ),
            "brand_identity": (
                "AI 기반 브랜드 전략 의사결정 시스템"
            ),
            "mission_statement": (
                "창업자가 자신만의 브랜드를 전략적으로 구축하도록 돕는다."
            ),
            "vision_statement": (
                "세계 최고의 AI Brand Decision Intelligence Platform이 된다."
            ),
            "core_values": (
                "Clarity, Trust, Strategic Thinking, Long-term Value"
            ),
            "positioning": (
                "단순 네이밍 툴이 아닌 AI 브랜드 전략 컨설턴트"
            ),
            "target_audience": (
                "브랜드 방향을 고민하는 초기 창업자"
            ),
            "brand_personality": (
                "Sage + Creator"
            ),
            "naming_strategy": (
                "의미와 전략성을 중심으로 브랜드명을 설계한다."
            ),
            "name_recommendations": [
                {
                    "name": name,
                    "meaning": "Origin + Intelligence",
                    "strategic_fit": (
                        "브랜드의 출발점과 전략적 사고를 상징"
                    ),
                    "strengths": (
                        "기억하기 쉽고 AI 브랜드 이미지가 강함"
                    ),
                    "weaknesses": (
                        "다소 기술 중심적으로 느껴질 수 있음"
                    ),
                    "score": 9,
                    "score_reason": (
                        "브랜드 전략과 AI 이미지를 동시에 전달"
                    ),
                }
                for name in candidate_names
            ],
            "final_recommendation": (
                f"{selected_name}을 최우선 후보로 추천합니다."
            ),
        }

        return json.dumps(report, ensure_ascii=False, indent=2)

    @staticmethod
    def _generate_intent_response(prompt: str) -> str:
        marker = "FOUNDER_DATA:\n"
        if marker not in prompt:
            raise ValueError("Mock intent prompt is missing FOUNDER_DATA")

        founder_data = json.loads(prompt.split(marker, 1)[1])
        signals = [
            {
                "kind": "objective",
                "concept": "problem_resolution",
                "weight": 0.3,
                "evidence": [founder_data["problem"]],
                "confidence": 0.9,
            },
            {
                "kind": "preference",
                "concept": "audience_focus",
                "weight": 0.2,
                "evidence": [founder_data["audience"]],
                "confidence": 0.9,
            },
            {
                "kind": "value",
                "concept": "founder_principles",
                "weight": 0.25,
                "evidence": [founder_data["principles"]],
                "confidence": 0.9,
            },
            {
                "kind": "preference",
                "concept": "distinct_approach",
                "weight": 0.25,
                "evidence": [founder_data["differentiation"]],
                "confidence": 0.85,
            },
        ]
        return json.dumps(
            {
                "signals": signals,
                "unresolved_signals": [],
            },
            ensure_ascii=False,
            indent=2,
        )

    @staticmethod
    def _extract_decision(prompt: str) -> tuple[str, list[str]]:
        selected_match = re.search(r"^Selected name:\s*(.+)$", prompt, re.MULTILINE)
        option_names = re.findall(
            r"^-\s+([^:]+):\s+total=",
            prompt,
            re.MULTILINE,
        )

        if selected_match and len(option_names) >= 5:
            selected = selected_match.group(1).strip()
            unique_names = list(dict.fromkeys(name.strip() for name in option_names))
            recommendations = [selected]
            recommendations.extend(
                name
                for name in unique_names
                if name.casefold() != selected.casefold()
            )
            return selected, recommendations[:5]

        fallback = [f"OriginIQ{i + 1}" for i in range(5)]
        return fallback[0], fallback
