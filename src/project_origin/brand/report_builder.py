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
            mission_statement=cls._mission_statement(profile, knowledge),
            vision_statement=profile.vision,
            core_values=cls._list_sentence(knowledge.core_values),
            positioning=knowledge.market_position,
            target_audience=knowledge.target_customer,
            brand_personality=knowledge.personality,
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
                evidence.brand_history_seed
                if evidence is not None
                else cls._fallback_origin_story(profile)
            ),
            brand_dna=cls._brand_dna(knowledge, decision),
            strategic_values=cls._strategic_values(profile, knowledge, decision),
            selected_name_rationale=decision.result.rationale,
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

    @staticmethod
    def _executive_summary(
        profile: FounderProfile,
        knowledge: BrandKnowledge,
        selected: DecisionOption,
    ) -> str:
        problem = BrandStrategyReportBuilder._clean_clause(profile.problem)
        position = BrandStrategyReportBuilder._clean_clause(
            knowledge.market_position
        )
        principles = BrandStrategyReportBuilder._clean_clause(
            profile.principles
        )
        return (
            f"This brand strategy translates the founder's problem, "
            f"{problem}, into a focused identity system for "
            f"{profile.audience}. The recommended name, {selected.label}, "
            f"anchors the brand around {position}, while preserving the "
            f"founder's principles: {principles}."
        )

    @staticmethod
    def _founder_insights(profile: FounderProfile) -> str:
        problem = BrandStrategyReportBuilder._clean_clause(profile.problem)
        differentiation = BrandStrategyReportBuilder._clean_clause(
            profile.differentiation
        )
        return (
            f"The founder is not only solving '{problem}'. The deeper "
            f"strategic tension is helping {profile.audience} move from "
            f"uncertainty to a clearer decision frame. The brand should make "
            f"{differentiation} feel tangible, credible, and repeatable."
        )

    @staticmethod
    def _mission_statement(
        profile: FounderProfile,
        knowledge: BrandKnowledge,
    ) -> str:
        problem = BrandStrategyReportBuilder._clean_clause(profile.problem)
        differentiation = BrandStrategyReportBuilder._clean_clause(
            profile.differentiation
        )
        principles = BrandStrategyReportBuilder._clean_clause(
            profile.principles
        )
        return (
            f"Help {profile.audience} solve {problem} through "
            f"{differentiation}, while protecting {principles}."
        )

    @staticmethod
    def _brand_identity(
        profile: FounderProfile,
        knowledge: BrandKnowledge,
    ) -> str:
        problem = BrandStrategyReportBuilder._clean_clause(profile.problem)
        vision = BrandStrategyReportBuilder._clean_clause(profile.vision)
        return (
            f"A {knowledge.personality} brand for {profile.audience}, built "
            f"around the shift from {problem} to {vision}."
        )

    @staticmethod
    def _naming_strategy(decision: BrandNamingDecisionRecord) -> str:
        evidence = decision.evidence
        if evidence is None:
            return decision.result.rationale

        return (
            "The naming strategy prioritizes strategic clarity over decorative "
            "novelty. The selected name is supported by "
            f"{'; '.join(evidence.selected_advantages)} while preserving room "
            "for future brand story, category education, and verbal identity."
        )

    @staticmethod
    def _name_recommendation(option: DecisionOption) -> NameRecommendation:
        return NameRecommendation(
            name=option.label,
            meaning=option.description or "Strategic naming candidate.",
            strategic_fit=(
                f"Strategic fit score: "
                f"{option.scores.get('strategic_fit', 0.0)}/10."
            ),
            strengths=(
                ", ".join(option.strengths)
                if option.strengths
                else "Balanced strategic and verbal qualities."
            ),
            weaknesses=(
                ", ".join(option.weaknesses)
                if option.weaknesses
                else "Requires external validation before launch."
            ),
            score=option.scores.get("total", 0.0),
            score_reason=(
                "Scored through the Project Origin naming rubric using "
                "pronunciation, originality, strategic fit, and memorability."
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
            f"Move forward with {selected.label}{confidence}. Treat this as a "
            "strategic working recommendation, then validate domain, trademark, "
            "multilingual meaning, and customer resonance before launch."
        )

    @staticmethod
    def _fallback_origin_story(profile: FounderProfile) -> str:
        return (
            f"The brand originates from a practical founder insight: "
            f"{profile.problem} The story should point toward {profile.vision}."
        )

    @staticmethod
    def _brand_dna(
        knowledge: BrandKnowledge,
        decision: BrandNamingDecisionRecord,
    ) -> str:
        evidence_dna = (
            decision.evidence.brand_dna if decision.evidence is not None else ()
        )
        dna = tuple(dict.fromkeys([*evidence_dna, *knowledge.identity_keywords]))
        return BrandStrategyReportBuilder._list_sentence(dna)

    @staticmethod
    def _strategic_values(
        profile: FounderProfile,
        knowledge: BrandKnowledge,
        decision: BrandNamingDecisionRecord,
    ) -> str:
        value_alignment = (
            decision.evidence.value_alignment
            if decision.evidence is not None
            else (profile.principles, knowledge.competitive_advantage)
        )
        return BrandStrategyReportBuilder._list_sentence(value_alignment)

    @staticmethod
    def _candidate_comparison(
        decision: BrandNamingDecisionRecord,
    ) -> str:
        evidence = decision.evidence
        if evidence is None or evidence.runner_up_name is None:
            return decision.result.rationale

        tradeoffs = (
            "; ".join(evidence.runner_up_tradeoffs)
            if evidence.runner_up_tradeoffs
            else "No major runner-up tradeoff was identified."
        )
        return (
            f"{evidence.selected_name} leads {evidence.runner_up_name} by "
            f"{evidence.score_delta} total-score points and "
            f"{evidence.strategy_delta} strategic-fit points. "
            f"Runner-up tradeoff: {tradeoffs}"
        )

    @staticmethod
    def _strategic_risks(decision: BrandNamingDecisionRecord) -> str:
        risks = (
            decision.evidence.risk_assessment
            if decision.evidence is not None
            else decision.result.warnings
        )
        return BrandStrategyReportBuilder._list_sentence(risks)

    @staticmethod
    def _next_action_plan(selected: DecisionOption) -> str:
        return (
            f"1. Run domain and trademark screening for {selected.label}. "
            "2. Test pronunciation and first impression with target customers. "
            "3. Develop a one-page verbal identity guide. "
            "4. Convert the brand DNA into homepage messaging, pitch language, "
            "and founder narrative."
        )

    @staticmethod
    def _list_sentence(values) -> str:
        cleaned = [str(value).strip() for value in values if str(value).strip()]
        return ", ".join(dict.fromkeys(cleaned))

    @staticmethod
    def _clean_clause(value: str) -> str:
        return str(value).strip().rstrip(".。")
