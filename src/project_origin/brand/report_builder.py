"""Build consultant-grade Brand Strategy Reports from structured evidence."""

from project_origin.brand.decision.models import BrandNamingDecisionRecord
from project_origin.brand.models import (
    BrandKnowledge,
    BrandStrategyReport,
    FounderProfile,
    NameRecommendation,
)
from project_origin.core import DecisionOption


class BrandStrategyReportBuilder:
    @classmethod
    def build(
        cls,
        profile: FounderProfile,
        knowledge: BrandKnowledge,
        decision: BrandNamingDecisionRecord,
    ) -> BrandStrategyReport:
        evidence = decision.evidence
        selected_option = cls._selected_option(decision)

        return BrandStrategyReport(
            executive_summary=cls._executive_summary(
                profile,
                knowledge,
                selected_option,
            ),
            founder_insights=cls._founder_insights(profile),
            brand_identity=cls._brand_identity(profile, knowledge),
            mission_statement=cls._mission_statement(profile),
            vision_statement=cls._clean_clause(profile.vision) + ".",
            core_values=cls._core_values(knowledge),
            positioning=cls._positioning(profile, knowledge),
            target_audience=knowledge.target_customer,
            brand_personality=cls._brand_personality(knowledge, profile),
            naming_strategy=cls._naming_strategy(decision),
            name_recommendations=[
                cls._name_recommendation(option)
                for option in decision.result.options[:5]
            ],
            final_recommendation=cls._final_recommendation(
                selected_option,
                decision,
            ),
            brand_origin_story=(
                cls._brand_origin_story(profile)
                if evidence is not None
                else cls._fallback_origin_story(profile)
            ),
            brand_dna=cls._brand_dna(knowledge, decision),
            strategic_values=cls._strategic_values(profile, knowledge, decision),
            selected_name_rationale=cls._selected_name_rationale(decision),
            candidate_comparison=cls._candidate_comparison(decision),
            strategic_risks=cls._strategic_risks(decision),
            next_action_plan=cls._next_action_plan(selected_option),
        )

    @staticmethod
    def _selected_option(decision: BrandNamingDecisionRecord) -> DecisionOption:
        return next(
            option
            for option in decision.result.options
            if option.identifier == decision.result.selected_option_id
        )

    @classmethod
    def _executive_summary(
        cls,
        profile: FounderProfile,
        knowledge: BrandKnowledge,
        selected: DecisionOption,
    ) -> str:
        problem = cls._clean_clause(profile.problem)
        position = cls._clean_clause(knowledge.market_position)
        principles = cls._clean_clause(profile.principles)
        return (
            f"The brand should help {profile.audience} move from a scattered "
            f"strategic problem ({problem}) to a clearer and more defensible "
            f"brand direction. {selected.label} is recommended as the naming "
            f"anchor because it supports the desired position: {position}. "
            f"The strategy should stay grounded in {principles}, so the brand "
            "feels useful, credible, and founder-led rather than merely "
            "decorative."
        )

    @classmethod
    def _founder_insights(cls, profile: FounderProfile) -> str:
        problem = cls._clean_clause(profile.problem)
        differentiation = cls._clean_clause(profile.differentiation)
        return (
            f"The visible problem is {problem}. Underneath it is a sharper "
            f"founder tension: {profile.audience} need confidence without "
            "losing control of the decision. The brand should therefore avoid "
            "sounding like a generic automation tool. It should make "
            f"{differentiation} feel tangible, credible, and repeatable."
        )

    @classmethod
    def _brand_origin_story(cls, profile: FounderProfile) -> str:
        problem = cls._clean_clause(profile.problem)
        vision = cls._clean_clause(profile.vision)
        return (
            f"The brand originates from a practical founder insight: {problem}. "
            f"Its story should not be about naming for naming's sake; it should "
            f"be about helping the audience move toward {vision}."
        )

    @classmethod
    def _brand_identity(
        cls,
        profile: FounderProfile,
        knowledge: BrandKnowledge,
    ) -> str:
        problem = cls._clean_clause(profile.problem)
        vision = cls._clean_clause(profile.vision)
        return (
            f"A {knowledge.personality} brand for {profile.audience}: calm "
            f"enough to build trust, but opinionated enough to guide decisions. "
            f"Its identity is built around the shift from {problem} to {vision}."
        )

    @classmethod
    def _mission_statement(cls, profile: FounderProfile) -> str:
        problem = cls._clean_clause(profile.problem)
        differentiation = cls._method_phrase(profile.differentiation)
        principles = cls._clean_clause(profile.principles)
        return (
            f"Give {profile.audience} a clearer way to resolve this challenge: "
            f"{problem}. The method is {differentiation}, protected by "
            f"{principles}."
        )

    @classmethod
    def _core_values(cls, knowledge: BrandKnowledge) -> str:
        return (
            "The core values should operate as decision filters: "
            f"{cls._prose_list(knowledge.core_values)}. Each future brand "
            "choice should be judged by whether it strengthens these values or "
            "dilutes them."
        )

    @classmethod
    def _positioning(
        cls,
        profile: FounderProfile,
        knowledge: BrandKnowledge,
    ) -> str:
        differentiation = cls._method_phrase(profile.differentiation)
        return (
            f"Position the brand for {profile.audience} as {knowledge.market_position} "
            f"The reason to choose it is clear: it is designed {differentiation}."
        )

    @staticmethod
    def _brand_personality(
        knowledge: BrandKnowledge,
        profile: FounderProfile,
    ) -> str:
        return (
            f"{knowledge.personality}. This archetype fits because the brand "
            f"must combine strategic judgment with creative expression for "
            f"{profile.audience}."
        )

    @classmethod
    def _naming_strategy(cls, decision: BrandNamingDecisionRecord) -> str:
        evidence = decision.evidence
        if evidence is None:
            return decision.result.rationale

        return (
            "The naming strategy should prioritize strategic clarity over "
            "decorative novelty. The name needs to be easy to say, credible in "
            "a serious product context, and flexible enough to carry a larger "
            "brand story. In the current decision set, the selected name is "
            f"supported by {cls._prose_list(evidence.selected_advantages)}."
        )

    @classmethod
    def _name_recommendation(cls, option: DecisionOption) -> NameRecommendation:
        return NameRecommendation(
            name=option.label,
            meaning=cls._candidate_meaning(option),
            strategic_fit=(
                f"{option.label} has a strategic-fit score of "
                f"{option.scores.get('strategic_fit', 0.0)}/10, indicating "
                "how strongly it reflects the intended brand direction."
            ),
            strengths=cls._candidate_strengths(option),
            weaknesses=cls._candidate_weaknesses(option),
            score=option.scores.get("total", 0.0),
            score_reason=(
                "The score combines pronunciation, originality, strategic fit, "
                "and memorability. It should guide prioritization, not replace "
                "domain, trademark, and customer validation."
            ),
        )

    @staticmethod
    def _final_recommendation(
        selected: DecisionOption,
        decision: BrandNamingDecisionRecord,
    ) -> str:
        confidence = (
            f" with decision confidence {decision.result.confidence}"
            if decision.result.confidence is not None
            else ""
        )
        return (
            f"Move forward with {selected.label}{confidence} as the working "
            "brand-name recommendation. Before launch, treat it like a strong "
            "strategic hypothesis: validate domain availability, trademark "
            "risk, multilingual meaning, and first-impression resonance with "
            "the target audience."
        )

    @staticmethod
    def _fallback_origin_story(profile: FounderProfile) -> str:
        return (
            f"The brand originates from a practical founder insight: "
            f"{profile.problem} The story should point toward {profile.vision}."
        )

    @classmethod
    def _brand_dna(
        cls,
        knowledge: BrandKnowledge,
        decision: BrandNamingDecisionRecord,
    ) -> str:
        evidence_dna = (
            decision.evidence.brand_dna if decision.evidence is not None else ()
        )
        dna = cls._dedupe_phrases([*evidence_dna, *knowledge.identity_keywords])
        return (
            f"The brand DNA should center on {cls._prose_list(dna)}. These cues "
            "should shape naming, voice, visual direction, and the first "
            "version of the founder narrative."
        )

    @classmethod
    def _strategic_values(
        cls,
        profile: FounderProfile,
        knowledge: BrandKnowledge,
        decision: BrandNamingDecisionRecord,
    ) -> str:
        principles = cls._clean_clause(profile.principles)
        method = cls._method_phrase(profile.differentiation)
        return (
            f"The strategic value system should emphasize {principles}. "
            f"Operationally, this means the brand must be able {method}. This "
            "keeps the brand anchored in the founder's actual operating logic, "
            "not just in attractive positioning language."
        )

    @classmethod
    def _selected_name_rationale(
        cls,
        decision: BrandNamingDecisionRecord,
    ) -> str:
        evidence = decision.evidence
        if evidence is None:
            return decision.result.rationale

        return (
            f"{evidence.selected_name} is recommended because it combines "
            f"{cls._prose_list(evidence.selected_advantages)}. The choice is "
            "not treated as final market proof; it is the strongest internal "
            "decision based on the available founder context and naming rubric."
        )

    @classmethod
    def _candidate_comparison(
        cls,
        decision: BrandNamingDecisionRecord,
    ) -> str:
        evidence = decision.evidence
        if evidence is None or evidence.runner_up_name is None:
            return decision.result.rationale

        tradeoffs = (
            cls._prose_list(evidence.runner_up_tradeoffs)
            if evidence.runner_up_tradeoffs
            else "no major runner-up tradeoff was identified"
        )
        return (
            f"{evidence.selected_name} leads {evidence.runner_up_name} by "
            f"{evidence.score_delta} total-score points and "
            f"{evidence.strategy_delta} strategic-fit points. The runner-up is "
            f"still viable, but the tradeoff is {tradeoffs}."
        )

    @classmethod
    def _strategic_risks(cls, decision: BrandNamingDecisionRecord) -> str:
        risks = (
            decision.evidence.risk_assessment
            if decision.evidence is not None
            else decision.result.warnings
        )
        return (
            f"{cls._prose_list(risks)}. The current recommendation should "
            "therefore be treated as a strategic naming direction, not as final "
            "legal or market clearance."
        )

    @staticmethod
    def _next_action_plan(selected: DecisionOption) -> str:
        return (
            f"1. Run domain and trademark screening for {selected.label}.\n"
            "2. Test pronunciation, recall, and first impression with target "
            "customers.\n"
            "3. Develop a one-page verbal identity guide covering tone, proof "
            "points, and phrases to avoid.\n"
            "4. Convert the brand DNA into homepage messaging, pitch language, "
            "and the founder narrative."
        )

    @staticmethod
    def _list_sentence(values) -> str:
        cleaned = [str(value).strip() for value in values if str(value).strip()]
        return ", ".join(dict.fromkeys(cleaned))

    @classmethod
    def _prose_list(cls, values) -> str:
        cleaned = [
            str(value).strip().rstrip(".")
            for value in values
            if str(value).strip()
        ]
        unique_values = list(dict.fromkeys(cleaned))
        if not unique_values:
            return ""
        if len(unique_values) == 1:
            return unique_values[0]
        if len(unique_values) == 2:
            return f"{unique_values[0]}, and {cls._lower_first(unique_values[1])}"
        return ", ".join(unique_values[:-1]) + f", and {unique_values[-1]}"

    @staticmethod
    def _dedupe_phrases(values) -> tuple[str, ...]:
        selected = []
        seen = set()
        for value in values:
            phrase = str(value).strip().rstrip(".")
            if not phrase:
                continue
            key = phrase.casefold()
            if any(key in existing or existing in key for existing in seen):
                continue
            selected.append(phrase)
            seen.add(key)
        return tuple(selected)

    @staticmethod
    def _lower_first(value: str) -> str:
        if not value:
            return value
        return value[0].lower() + value[1:]

    @staticmethod
    def _candidate_meaning(option: DecisionOption) -> str:
        pattern = option.metadata.get("generation_pattern", "structured naming")
        roots = option.metadata.get("generation_roots", ())
        root_phrase = (
            f" using the root cues {BrandStrategyReportBuilder._prose_list(roots)}"
            if roots
            else ""
        )
        return (
            f"{option.label} is a {str(pattern).replace('_', ' ')} candidate"
            f"{root_phrase}. Its role is to make the brand direction easier to "
            "remember without losing strategic seriousness."
        )

    @staticmethod
    def _candidate_strengths(option: DecisionOption) -> str:
        if option.strengths:
            return BrandStrategyReportBuilder._prose_list(option.strengths) + "."
        return (
            "Balanced verbal qualities with no single obvious weakness in the "
            "current scoring rubric."
        )

    @staticmethod
    def _candidate_weaknesses(option: DecisionOption) -> str:
        if option.weaknesses:
            return BrandStrategyReportBuilder._prose_list(option.weaknesses) + "."
        return (
            "No internal red flag was detected, but external validation is "
            "still required before launch."
        )

    @staticmethod
    def _clean_clause(value: str) -> str:
        return str(value).strip().rstrip(".")

    @staticmethod
    def _method_phrase(value: str) -> str:
        cleaned = str(value).strip().rstrip(".")
        lowered = cleaned.casefold()
        if lowered.startswith("turns "):
            return "to turn " + cleaned[6:]
        if lowered.startswith("creates "):
            return "to create " + cleaned[8:]
        if lowered.startswith("helps "):
            return "to help " + cleaned[6:]
        return cleaned
