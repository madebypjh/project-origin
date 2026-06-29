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

        if "TASK: BRAND_LIST_EXPANSION_V1" in prompt:
            return self._generate_brand_list_expansion_response(prompt)

        if "TASK: INTENT_INTERPRETATION_V1" in prompt:
            return self._generate_intent_response(prompt)

        if "# Brand Analysis Prompt" in prompt:
            return self._generate_brand_analysis_response(prompt)

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
        case_signals = MockProvider._case_specific_intent_signals(founder_data)
        if case_signals is not None:
            return json.dumps(
                {
                    "signals": case_signals,
                    "unresolved_signals": [],
                },
                ensure_ascii=False,
                indent=2,
            )

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
    def _case_specific_intent_signals(
        founder_data: dict,
    ) -> list[dict] | None:
        text = " ".join(str(value) for value in founder_data.values()).casefold()

        if "trusted decision layer" in text:
            return [
                {
                    "kind": "positioning",
                    "concept": "trusted_decision_layer",
                    "weight": 0.34,
                    "evidence": [founder_data["vision"]],
                    "confidence": 0.9,
                },
                {
                    "kind": "value",
                    "concept": "operator_control",
                    "weight": 0.33,
                    "evidence": ["operator control"],
                    "confidence": 0.9,
                },
                {
                    "kind": "capability",
                    "concept": "explainable_prioritization",
                    "weight": 0.33,
                    "evidence": ["explainable priorities"],
                    "confidence": 0.85,
                },
            ]

        if "medical humility" in text:
            return [
                {
                    "kind": "value",
                    "concept": "medical_humility",
                    "weight": 0.34,
                    "evidence": [
                        "medical humility",
                        founder_data["problem"],
                    ],
                    "confidence": 0.9,
                },
                {
                    "kind": "desired_emotion",
                    "concept": "humane_guidance",
                    "weight": 0.33,
                    "evidence": [
                        "understandable and humane",
                        founder_data["vision"],
                    ],
                    "confidence": 0.85,
                },
                {
                    "kind": "constraint",
                    "concept": "non_clinician_replacement",
                    "weight": 0.33,
                    "evidence": [
                        "without pretending to replace clinicians",
                        founder_data["differentiation"],
                    ],
                    "confidence": 0.9,
                },
            ]

        if "financial clarity" in text:
            return [
                {
                    "kind": "audience",
                    "concept": "first_time_founders",
                    "weight": 0.34,
                    "evidence": ["First-time founders"],
                    "confidence": 0.9,
                },
                {
                    "kind": "outcome",
                    "concept": "financial_clarity",
                    "weight": 0.33,
                    "evidence": ["financial clarity"],
                    "confidence": 0.9,
                },
                {
                    "kind": "value",
                    "concept": "responsible_guidance",
                    "weight": 0.33,
                    "evidence": ["responsible guidance"],
                    "confidence": 0.85,
                },
            ]

        if "creator ownership" in text:
            return [
                {
                    "kind": "audience",
                    "concept": "independent_creators",
                    "weight": 0.34,
                    "evidence": ["independent writers and video creators"],
                    "confidence": 0.9,
                },
                {
                    "kind": "value",
                    "concept": "creator_ownership",
                    "weight": 0.33,
                    "evidence": ["creator ownership"],
                    "confidence": 0.9,
                },
                {
                    "kind": "differentiation",
                    "concept": "preserving_individual_voice",
                    "weight": 0.33,
                    "evidence": ["preserving individual voice"],
                    "confidence": 0.85,
                },
            ]

        if "material-level provenance" in text:
            return [
                {
                    "kind": "audience",
                    "concept": "industrial_procurement",
                    "weight": 0.34,
                    "evidence": ["procurement teams"],
                    "confidence": 0.9,
                },
                {
                    "kind": "value",
                    "concept": "traceability",
                    "weight": 0.33,
                    "evidence": ["Traceability"],
                    "confidence": 0.9,
                },
                {
                    "kind": "differentiation",
                    "concept": "material_level_provenance",
                    "weight": 0.33,
                    "evidence": ["material-level provenance"],
                    "confidence": 0.85,
                },
            ]

        if "confidence-building" in text:
            return [
                {
                    "kind": "audience",
                    "concept": "middle_school_learners",
                    "weight": 0.34,
                    "evidence": ["middle school learners"],
                    "confidence": 0.9,
                },
                {
                    "kind": "desired_emotion",
                    "concept": "confidence_building_learning",
                    "weight": 0.33,
                    "evidence": ["confidence-building"],
                    "confidence": 0.85,
                },
                {
                    "kind": "constraint",
                    "concept": "non_shaming_guidance",
                    "weight": 0.33,
                    "evidence": ["without shaming students"],
                    "confidence": 0.9,
                },
            ]

        if "respecting attorney boundaries" in text:
            return [
                {
                    "kind": "audience",
                    "concept": "small_business_owners",
                    "weight": 0.34,
                    "evidence": ["small business owners"],
                    "confidence": 0.9,
                },
                {
                    "kind": "constraint",
                    "concept": "attorney_boundary_respect",
                    "weight": 0.33,
                    "evidence": ["respecting attorney boundaries"],
                    "confidence": 0.9,
                },
                {
                    "kind": "capability",
                    "concept": "plain_language_clause_risk",
                    "weight": 0.33,
                    "evidence": ["risky clauses in plain language"],
                    "confidence": 0.85,
                },
            ]

        if "scientific humility" in text:
            return [
                {
                    "kind": "audience",
                    "concept": "municipal_resilience_teams",
                    "weight": 0.34,
                    "evidence": ["municipal infrastructure"],
                    "confidence": 0.9,
                },
                {
                    "kind": "value",
                    "concept": "scientific_humility",
                    "weight": 0.33,
                    "evidence": ["Scientific humility"],
                    "confidence": 0.9,
                },
                {
                    "kind": "capability",
                    "concept": "asset_level_planning",
                    "weight": 0.33,
                    "evidence": ["asset-level planning decisions"],
                    "confidence": 0.85,
                },
            ]

        if "parents of preteens" in text:
            return [
                {
                    "kind": "audience",
                    "concept": "parents_of_preteens",
                    "weight": 0.34,
                    "evidence": ["parents of preteens"],
                    "confidence": 0.9,
                },
                {
                    "kind": "value",
                    "concept": "privacy_preserving_safety",
                    "weight": 0.33,
                    "evidence": ["without invading children's privacy"],
                    "confidence": 0.9,
                },
                {
                    "kind": "constraint",
                    "concept": "non_surveillance_parenting",
                    "weight": 0.33,
                    "evidence": [
                        "without turning parenting into surveillance"
                    ],
                    "confidence": 0.85,
                },
            ]

        if "operator oversight" in text:
            return [
                {
                    "kind": "audience",
                    "concept": "enterprise_operations_leaders",
                    "weight": 0.34,
                    "evidence": ["enterprise operations leaders"],
                    "confidence": 0.9,
                },
                {
                    "kind": "value",
                    "concept": "operator_oversight",
                    "weight": 0.33,
                    "evidence": ["operator oversight"],
                    "confidence": 0.9,
                },
                {
                    "kind": "constraint",
                    "concept": "human_control_of_exceptions",
                    "weight": 0.33,
                    "evidence": ["humans in control of exceptions"],
                    "confidence": 0.85,
                },
            ]

        if "privacy-conscious mobile consumers" in text:
            return [
                {
                    "kind": "audience",
                    "concept": "privacy_conscious_consumers",
                    "weight": 0.34,
                    "evidence": ["privacy-conscious mobile consumers"],
                    "confidence": 0.9,
                },
                {
                    "kind": "value",
                    "concept": "user_controlled_personalization",
                    "weight": 0.33,
                    "evidence": ["user-controlled"],
                    "confidence": 0.9,
                },
                {
                    "kind": "constraint",
                    "concept": "no_behavioral_profile_sales",
                    "weight": 0.33,
                    "evidence": ["without selling behavioral profiles"],
                    "confidence": 0.85,
                },
            ]

        if "platform lock-in" in text:
            return [
                {
                    "kind": "audience",
                    "concept": "independent_creators",
                    "weight": 0.34,
                    "evidence": ["Independent creators"],
                    "confidence": 0.9,
                },
                {
                    "kind": "value",
                    "concept": "creator_ownership",
                    "weight": 0.33,
                    "evidence": ["ownership"],
                    "confidence": 0.9,
                },
                {
                    "kind": "constraint",
                    "concept": "no_platform_lock_in",
                    "weight": 0.33,
                    "evidence": ["without platform lock-in"],
                    "confidence": 0.85,
                },
            ]

        if "human authority" in text:
            return [
                {
                    "kind": "audience",
                    "concept": "warehouse_operations_managers",
                    "weight": 0.34,
                    "evidence": ["warehouse operations managers"],
                    "confidence": 0.9,
                },
                {
                    "kind": "value",
                    "concept": "human_authority",
                    "weight": 0.33,
                    "evidence": ["human authority"],
                    "confidence": 0.9,
                },
                {
                    "kind": "capability",
                    "concept": "fleet_signal_decisions",
                    "weight": 0.33,
                    "evidence": ["robot fleet signals"],
                    "confidence": 0.85,
                },
            ]

        if "pretending to be therapy" in text:
            return [
                {
                    "kind": "audience",
                    "concept": "adults_managing_stress",
                    "weight": 0.34,
                    "evidence": ["adults managing everyday stress"],
                    "confidence": 0.9,
                },
                {
                    "kind": "constraint",
                    "concept": "not_therapy",
                    "weight": 0.33,
                    "evidence": [
                        "not want an app pretending to be therapy"
                    ],
                    "confidence": 0.9,
                },
                {
                    "kind": "value",
                    "concept": "professional_boundaries",
                    "weight": 0.33,
                    "evidence": ["professional boundaries"],
                    "confidence": 0.85,
                },
            ]

        if "clear escalation" in text:
            return [
                {
                    "kind": "audience",
                    "concept": "supply_chain_teams",
                    "weight": 0.34,
                    "evidence": ["supply chain and logistics teams"],
                    "confidence": 0.9,
                },
                {
                    "kind": "value",
                    "concept": "clear_escalation",
                    "weight": 0.33,
                    "evidence": ["clear escalation"],
                    "confidence": 0.9,
                },
                {
                    "kind": "capability",
                    "concept": "prioritized_operational_decisions",
                    "weight": 0.33,
                    "evidence": ["prioritized operational decisions"],
                    "confidence": 0.85,
                },
            ]

        return None

    @staticmethod
    def _generate_brand_list_expansion_response(prompt: str) -> str:
        marker = "CATEGORIES:\n"
        end_marker = "\n\nEXISTING_BRANDS:"
        if marker not in prompt or end_marker not in prompt:
            raise ValueError("Mock brand expansion prompt is malformed")

        raw_categories = prompt.split(marker, 1)[1].split(end_marker, 1)[0]
        categories = json.loads(raw_categories)
        proposals = []
        for category in categories:
            normalized = str(category).replace("_", " ").title().replace(" ", "")
            proposals.append(
                {
                    "category": category,
                    "brands": [
                        f"{normalized}Nova",
                        f"{normalized}Forge",
                        f"{normalized}Pilot",
                    ],
                }
            )

        return json.dumps({"categories": proposals}, ensure_ascii=False, indent=2)

    @staticmethod
    def _generate_brand_analysis_response(prompt: str) -> str:
        marker = "Input:\n\n"
        end_marker = "\n\n---"
        if marker not in prompt or end_marker not in prompt:
            raise ValueError("Mock brand analysis prompt is malformed")

        raw_brands = prompt.split(marker, 1)[1].split(end_marker, 1)[0]
        brands = [
            line.removeprefix("-").strip()
            for line in raw_brands.splitlines()
            if line.strip().startswith("-")
        ]
        return json.dumps(
            [
                {
                    "name": brand,
                    "industry": "mock research",
                    "country": "unknown",
                    "founded_year": 2000,
                    "style": "invented",
                    "name_origin": "inferred mock analysis",
                    "semantic_density": "medium",
                    "semantic_category": "abstract",
                    "brand_archetype": "Creator",
                    "emotional_tone": "trustworthy",
                    "phonetic_pattern": "CVCVC",
                    "syllables": MockProvider._mock_syllables(brand),
                    "vowel_ratio": 0.45,
                    "hard_consonant_ratio": 0.3,
                    "soft_consonant_ratio": 0.3,
                    "pronunciation_difficulty": 3,
                    "memorability_score": 8,
                    "distinctiveness_score": 8,
                    "innovation_score": 7,
                    "trust_score": 7,
                    "premium_score": 5,
                    "playfulness_score": 4,
                    "global_scalability_score": 8,
                    "morphology_type": "abstract coined word",
                    "linguistic_style": "short global brand",
                    "notes": "Mock analysis for deterministic tests.",
                }
                for brand in brands
            ],
            ensure_ascii=False,
            indent=2,
        )

    @staticmethod
    def _mock_syllables(brand: str) -> list[str]:
        compact = re.sub(r"[^A-Za-z0-9]+", "", brand).lower()
        if not compact:
            return [brand]
        midpoint = max(1, len(compact) // 2)
        return [compact[:midpoint], compact[midpoint:]]

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
