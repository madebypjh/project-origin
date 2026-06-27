"""
Project Origin - Prompt Builder v2

Builds a structured LLM prompt using:
- FounderProfile
- Reasoning Frameworks
- Strict JSON output schema
"""

from .models import FounderProfile
from .frameworks import ReasoningFrameworks


class PromptBuilder:
    @staticmethod
    def build(profile: FounderProfile) -> str:
        reasoning_frameworks = ReasoningFrameworks.build_all()

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
Reasoning Frameworks
==============================

{reasoning_frameworks}

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
- final_recommendation: Choose the best name and explain why.

Every major conclusion must be grounded in the founder profile.
"""