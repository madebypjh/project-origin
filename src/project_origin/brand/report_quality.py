"""Automatic quality checks for Brand Strategy Reports.

The evaluator is intentionally rule-based. Its job is not to judge taste like
an expert human reviewer, but to catch reports that lack the minimum structure,
evidence, actionability, and decision alignment expected from Project Origin.
"""

from dataclasses import dataclass

from project_origin.brand.decision.models import BrandNamingDecisionRecord
from project_origin.brand.models import BrandStrategyReport, FounderProfile


@dataclass(frozen=True)
class ReportQualityPillarScore:
    name: str
    score: int
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class ReportQualityResult:
    pillar_scores: tuple[ReportQualityPillarScore, ...]
    total_score: int
    max_score: int
    passed: bool
    automatic_failures: tuple[str, ...]
    missing_sections: tuple[str, ...]

    @property
    def average_score(self) -> float:
        if not self.pillar_scores:
            return 0.0
        return round(self.total_score / len(self.pillar_scores), 2)


class ReportQualityEvaluator:
    REQUIRED_SECTIONS = {
        "executive_summary": "Executive Summary",
        "founder_insights": "Founder Insights",
        "brand_origin_story": "Brand Origin Story",
        "brand_identity": "Brand Identity",
        "brand_dna": "Brand DNA",
        "mission_statement": "Mission Statement",
        "vision_statement": "Vision Statement",
        "core_values": "Core Values",
        "strategic_values": "Strategic Values",
        "positioning": "Positioning",
        "target_audience": "Target Audience",
        "brand_personality": "Brand Personality",
        "naming_strategy": "Naming Strategy",
        "selected_name_rationale": "Selected Name Rationale",
        "candidate_comparison": "Candidate Comparison",
        "final_recommendation": "Final Recommendation",
        "strategic_risks": "Strategic Risks",
        "next_action_plan": "Next Action Plan",
    }
    PASSING_SCORE = 22
    MAX_SCORE = 25

    @classmethod
    def evaluate(
        cls,
        report: BrandStrategyReport,
        profile: FounderProfile,
        decision: BrandNamingDecisionRecord | None = None,
    ) -> ReportQualityResult:
        missing_sections = cls._missing_sections(report)
        automatic_failures = cls._automatic_failures(
            report,
            profile,
            decision,
            missing_sections,
        )
        pillar_scores = (
            cls._score_strategic_depth(report, profile),
            cls._score_evidence_based_reasoning(report, profile, decision),
            cls._score_originality(report),
            cls._score_actionability(report, decision),
            cls._score_professional_presentation(report, missing_sections),
        )
        total_score = sum(score.score for score in pillar_scores)

        return ReportQualityResult(
            pillar_scores=pillar_scores,
            total_score=total_score,
            max_score=cls.MAX_SCORE,
            passed=(
                total_score >= cls.PASSING_SCORE
                and not automatic_failures
                and not missing_sections
            ),
            automatic_failures=automatic_failures,
            missing_sections=missing_sections,
        )

    @classmethod
    def _score_strategic_depth(
        cls,
        report: BrandStrategyReport,
        profile: FounderProfile,
    ) -> ReportQualityPillarScore:
        checks = {
            "connects problem to strategy": profile.problem in (
                report.executive_summary + report.brand_origin_story
            ),
            "explains founder tension": cls._contains_any(
                report.founder_insights,
                ("tension", "uncertainty", "decision frame", "motivation"),
            ),
            "defines positioning": bool(report.positioning.strip()),
            "expresses differentiation": profile.differentiation in (
                report.founder_insights
                + report.mission_statement
                + report.strategic_values
            ),
            "connects long-term vision": profile.vision in (
                report.brand_origin_story + report.vision_statement
            ),
        }
        return cls._pillar("Strategic Depth", checks)

    @classmethod
    def _score_evidence_based_reasoning(
        cls,
        report: BrandStrategyReport,
        profile: FounderProfile,
        decision: BrandNamingDecisionRecord | None,
    ) -> ReportQualityPillarScore:
        selected_name = cls._selected_name(decision)
        checks = {
            "uses founder evidence": cls._contains_any(
                report.executive_summary + report.mission_statement,
                (profile.audience, profile.principles),
            ),
            "uses decision evidence": cls._contains_any(
                report.selected_name_rationale,
                ("total score", "strategic fit", "decision evidence"),
            ),
            "includes candidate tradeoff": cls._contains_any(
                report.candidate_comparison,
                ("tradeoff", "runner-up", "leads"),
            ),
            "separates risks": cls._contains_any(
                report.strategic_risks,
                ("domain", "trademark", "validation", "screening"),
            ),
            "preserves selected decision": (
                selected_name is None
                or selected_name in report.final_recommendation
            ),
        }
        return cls._pillar("Evidence-Based Reasoning", checks)

    @classmethod
    def _score_originality(
        cls,
        report: BrandStrategyReport,
    ) -> ReportQualityPillarScore:
        full_text = cls._full_text(report).casefold()
        generic_terms = (
            "innovative solution",
            "cutting edge",
            "game changer",
            "next generation",
            "one stop",
            "best in class",
        )
        checks = {
            "contains brand DNA": bool(report.brand_dna.strip()),
            "contains structured brand DNA": len(report.brand_dna_items) >= 3,
            "contains origin story": bool(report.brand_origin_story.strip()),
            "contains naming philosophy": cls._contains_any(
                report.naming_strategy,
                ("clarity", "novelty", "tone", "linguistic", "story"),
            ),
            "avoids dominant buzzwords": not any(
                term in full_text for term in generic_terms
            ),
        }
        return cls._pillar("Originality", checks)

    @classmethod
    def _score_actionability(
        cls,
        report: BrandStrategyReport,
        decision: BrandNamingDecisionRecord | None,
    ) -> ReportQualityPillarScore:
        selected_name = cls._selected_name(decision)
        checks = {
            "has exactly five candidates": len(report.name_recommendations) == 5,
            "has final recommendation": bool(
                report.final_recommendation.strip()
            ),
            "final recommendation names selection": (
                selected_name is None
                or selected_name in report.final_recommendation
            ),
            "has next action plan": cls._contains_any(
                report.next_action_plan,
                ("1.", "2.", "domain", "trademark", "test"),
            ),
            "has structured value rules": len(report.strategic_value_items) >= 3,
        }
        return cls._pillar("Actionability", checks)

    @classmethod
    def _score_professional_presentation(
        cls,
        report: BrandStrategyReport,
        missing_sections: tuple[str, ...],
    ) -> ReportQualityPillarScore:
        checks = {
            "no missing required sections": not missing_sections,
            "all candidates have complete details": all(
                [
                    item.meaning,
                    item.strategic_fit,
                    item.strengths,
                    item.weaknesses,
                    item.score_reason,
                ]
                for item in report.name_recommendations
            ),
            "candidate scores are valid": all(
                0 <= item.score <= 10 for item in report.name_recommendations
            ),
            "clear report structure": len(report.to_dict()) >= 18,
            "readable section lengths": cls._readable_lengths(report),
        }
        return cls._pillar("Professional Presentation", checks)

    @classmethod
    def _automatic_failures(
        cls,
        report: BrandStrategyReport,
        profile: FounderProfile,
        decision: BrandNamingDecisionRecord | None,
        missing_sections: tuple[str, ...],
    ) -> tuple[str, ...]:
        failures = []
        selected_name = cls._selected_name(decision)

        if missing_sections:
            failures.append("required report sections are missing")
        if len(report.name_recommendations) != 5:
            failures.append("report must include exactly five name candidates")
        if selected_name and selected_name not in report.final_recommendation:
            failures.append("final recommendation is not aligned to decision")
        if profile.problem not in cls._full_text(report):
            failures.append("report does not preserve founder problem evidence")
        if not report.next_action_plan.strip():
            failures.append("report lacks concrete next actions")

        return tuple(failures)

    @classmethod
    def _missing_sections(cls, report: BrandStrategyReport) -> tuple[str, ...]:
        missing = []
        for field_name, label in cls.REQUIRED_SECTIONS.items():
            value = getattr(report, field_name, "")
            if not str(value).strip():
                missing.append(label)
        return tuple(missing)

    @staticmethod
    def _pillar(
        name: str,
        checks: dict[str, bool],
    ) -> ReportQualityPillarScore:
        passed_reasons = tuple(
            reason for reason, passed in checks.items() if passed
        )
        return ReportQualityPillarScore(
            name=name,
            score=sum(1 for passed in checks.values() if passed),
            reasons=passed_reasons,
        )

    @staticmethod
    def _selected_name(
        decision: BrandNamingDecisionRecord | None,
    ) -> str | None:
        if decision is None:
            return None
        return next(
            option.label
            for option in decision.result.options
            if option.identifier == decision.result.selected_option_id
        )

    @staticmethod
    def _contains_any(value: str, needles: tuple[str, ...]) -> bool:
        normalized_value = value.casefold()
        return any(needle.casefold() in normalized_value for needle in needles)

    @staticmethod
    def _full_text(report: BrandStrategyReport) -> str:
        values = []
        for value in report.to_dict().values():
            if isinstance(value, list):
                values.extend(str(item) for item in value)
            else:
                values.append(str(value))
        return " ".join(values)

    @staticmethod
    def _repetition_ratio(text: str) -> float:
        words = [
            word.strip(".,:;!?()[]{}\"'").casefold()
            for word in text.split()
            if len(word.strip(".,:;!?()[]{}\"'")) >= 6
        ]
        if not words:
            return 0.0
        repeated_count = len(words) - len(set(words))
        return repeated_count / len(words)

    @staticmethod
    def _readable_lengths(report: BrandStrategyReport) -> bool:
        section_values = [
            report.executive_summary,
            report.founder_insights,
            report.brand_origin_story,
            report.brand_identity,
            report.mission_statement,
            report.naming_strategy,
            report.final_recommendation,
        ]
        return all(40 <= len(value.strip()) <= 700 for value in section_values)
