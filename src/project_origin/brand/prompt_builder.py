"""
Project Origin - Prompt Builder v3

Builds a structured LLM prompt using:
- FounderProfile and BrandKnowledge
- Reasoning Frameworks
- An explainable DecisionResult from the Naming Engine
- Strict JSON output schema
"""

from project_origin.brand.frameworks import ReasoningFrameworks
from project_origin.brand.models import BrandKnowledge, FounderProfile
from project_origin.core import DecisionResult


class PromptBuilder:
    @staticmethod
    def build(
        profile: FounderProfile,
        knowledge: BrandKnowledge,
        decision: DecisionResult,
    ) -> str:
        reasoning_frameworks = ReasoningFrameworks.build_all()
        candidate_section = PromptBuilder._build_candidate_section(decision)

        return f"""
You are a senior brand strategy consultant.

Your job is to create a professional Brand Strategy Report.

Do not act as a simple name generator.
Do not provide generic advice.
Do not invent facts that are not supported by the founder profile.

If information is missing, write "추가 정보 필요".

Write the report in Korean.
Brand name candidates may be written in English if appropriate.

==============================
Founder Profile
==============================

Problem:
{profile.problem}

Target Audience:
{profile.audience}

Long-term Vision:
{profile.vision}

Core Principles:
{profile.principles}

Differentiation:
{profile.differentiation}

==============================
Structured Brand Knowledge
==============================

Purpose:
{knowledge.purpose}

Method:
{knowledge.method}

Identity:
{knowledge.identity}

Market Position:
{knowledge.market_position}

Competitive Advantage:
{knowledge.competitive_advantage}

==============================
Reasoning Frameworks
==============================

{reasoning_frameworks}

{candidate_section}

==============================
Output Rules
==============================

Return ONLY valid JSON.

Do not include markdown.
Do not include explanations outside the JSON.
Do not wrap the JSON in code blocks.

Use this exact JSON schema:

{{
  "executive_summary": "",
  "founder_insights": "",
  "brand_identity": "",
  "mission_statement": "",
  "vision_statement": "",
  "core_values": "",
  "positioning": "",
  "target_audience": "",
  "brand_personality": "",
  "naming_strategy": "",
  "name_recommendations": [
    {{
      "name": "",
      "meaning": "",
      "strategic_fit": "",
      "strengths": "",
      "weaknesses": "",
      "score": 0,
      "score_reason": ""
    }}
  ],
  "final_recommendation": ""
}}

==============================
Depth Requirements
==============================

- executive_summary: 3~5 sentences.
- founder_insights: Explain the deeper founder intent.
- brand_identity: Define the brand's essence clearly.
- mission_statement: One concise mission statement.
- vision_statement: One long-term vision statement.
- core_values: 3~5 values with short explanations.
- positioning: Explain who the brand is for and why it should be chosen.
- target_audience: Describe the ideal customer.
- brand_personality: Select and explain the best brand archetype.
- naming_strategy: Explain the naming direction.
- name_recommendations: Provide exactly 5 candidates.
- final_recommendation: Explain Project Origin's selected name. Do not replace it.

Every major conclusion must be grounded in the founder profile.
"""

    @staticmethod
    def _build_candidate_section(decision: DecisionResult) -> str:
        selected = next(
            option
            for option in decision.options
            if option.identifier == decision.selected_option_id
        )
        candidates = "\n".join(
            (
                f"- {option.label}: total={option.scores.get('total', 0)}/10, "
                f"strategic_fit={option.scores.get('strategic_fit', 0)}/10"
            )
            for option in decision.options
        )

        return f"""
==============================
Project Origin Naming Decision
==============================

Selected name: {selected.label}
Decision rationale: {decision.rationale}
Decision confidence: {decision.confidence}

The following options were generated and evaluated by Project Origin:

{candidates}

Rules:
- Recommend exactly 5 names from the provided options.
- Include {selected.label} among the 5 recommendations.
- The final recommendation must remain {selected.label}.
- Do not invent replacement candidates.
- Explain the existing decision; do not silently make a new decision.
"""
