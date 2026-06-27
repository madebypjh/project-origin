"""
Project Origin
Prompt Builder

Converts structured FounderProfile into
a professional AI prompt.
"""

from .models import FounderProfile


class PromptBuilder:

    @staticmethod
    def build(profile: FounderProfile) -> str:

        return f"""
You are one of the world's leading brand strategists.

Your task is NOT to simply generate company names.

Your task is to deeply understand the founder's intent,
business philosophy, long-term vision, and competitive positioning.

Produce a strategic branding report.

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
Instructions
==============================

Analyze the founder profile carefully.

Think step by step.

Do not invent facts.

Explain your reasoning.

Return the following sections.

1. Executive Summary

2. Founder Analysis

3. Brand DNA

4. Mission Statement

5. Brand Positioning

6. Brand Narrative

7. Naming Strategy

8. Five Brand Name Recommendations

9. Final Recommendation
"""