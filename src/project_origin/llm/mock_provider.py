"""
Project Origin - Mock LLM Provider

Provides a deterministic mock response for development and testing.
"""

import json

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
                    "name": f"OriginIQ{i + 1}",
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
                for i in range(5)
            ],
            "final_recommendation": (
                "OriginIQ1을 최우선 후보로 추천합니다."
            ),
        }

        return json.dumps(report, ensure_ascii=False, indent=2)