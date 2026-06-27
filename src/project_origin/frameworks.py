"""
Project Origin - Reasoning Frameworks

This module does not analyze founder data directly.
It defines reasoning rules, evaluation criteria, and strategic frameworks
that PromptBuilder can use to guide the LLM.
"""


class GoldenCircleFramework:
    @staticmethod
    def instructions() -> str:
        return """
Golden Circle:
- Identify WHY the company exists.
- Identify HOW the company creates value.
- Identify WHAT the company actually provides.
- Do not simply repeat the founder's words.
- Infer the deeper motivation behind the founder's answers.
- If the information is insufficient, write "추가 정보 필요".
"""


class BrandDNAFramework:
    @staticmethod
    def instructions() -> str:
        return """
Brand DNA:
- Extract the core identity of the brand.
- Identify purpose, values, personality, and differentiation.
- Avoid generic values unless they are clearly supported by the founder's answers.
- Every conclusion must be grounded in the interview response.
"""


class PositioningFramework:
    @staticmethod
    def instructions() -> str:
        return """
Brand Positioning:
- Define who the brand is for.
- Define what alternative the customer would otherwise choose.
- Define why this brand should be chosen.
- Avoid using generic positioning such as "AI consultant" unless directly relevant.
"""


class ArchetypeFramework:
    @staticmethod
    def definitions() -> str:
        return """
Brand Archetypes:
- Sage: knowledge, insight, truth, analysis
- Creator: creation, design, imagination, originality
- Hero: challenge, courage, achievement, problem-solving
- Explorer: discovery, freedom, exploration, independence
- Ruler: leadership, control, authority, premium status
- Caregiver: protection, support, service, empathy
- Magician: transformation, vision, possibility, innovation
- Outlaw: rebellion, disruption, breaking conventions
- Lover: beauty, emotion, desire, intimacy
- Jester: fun, humor, playfulness, entertainment
- Everyman: simplicity, familiarity, accessibility
- Innocent: purity, optimism, trust, simplicity

Select the best-fitting archetype based on the full founder profile.
Always explain why the archetype fits.
Do not rely on keyword matching alone.
"""


class ValuePropositionFramework:
    @staticmethod
    def instructions() -> str:
        return """
Value Proposition:
- Identify the customer's main problem.
- Identify the value the company provides.
- Explain why the solution matters.
- Connect the value proposition to the founder's long-term vision.
"""


class NamingEvaluationFramework:
    @staticmethod
    def criteria() -> list[str]:
        return [
            "Meaning",
            "Memorability",
            "Pronunciation",
            "Strategic Alignment",
            "Scalability",
            "Emotional Impact",
            "Founder Intent Fit",
        ]

    @staticmethod
    def instructions() -> str:
        criteria_text = ", ".join(NamingEvaluationFramework.criteria())

        return f"""
Naming Evaluation:
Evaluate each brand name candidate using these criteria:

{criteria_text}

For each name candidate, provide:
- Meaning
- Strategic fit
- Strengths
- Weaknesses
- Score out of 10
- Reason for the score

Do not recommend names only because they sound good.
Every recommendation must connect to the founder's intent and brand strategy.
"""


class ReasoningFrameworks:
    @staticmethod
    def build_all() -> str:
        return "\n\n".join(
            [
                GoldenCircleFramework.instructions(),
                BrandDNAFramework.instructions(),
                PositioningFramework.instructions(),
                ArchetypeFramework.definitions(),
                ValuePropositionFramework.instructions(),
                NamingEvaluationFramework.instructions(),
            ]
        )