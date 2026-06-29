"""Markdown reports for blinded human review of naming benchmark outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from benchmarks.brand_naming.loader import load_cases


class BlindReviewMarkdownReport:
    @classmethod
    def from_json_file(cls, path: Path) -> str:
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls.from_report_data(data)

    @classmethod
    def from_report_data(cls, data: dict[str, Any]) -> str:
        benchmark_cases = {case.identifier: case for case in load_cases()}
        lines = [
            "# Brand Naming Blind Review",
            "",
            "This report hides which candidate set came from the active path and "
            "which came from the intent-shadow path. Reviewers should judge the "
            "sets before checking the answer key.",
            "",
            "## Review rubric",
            "",
            "Score each set from 1 to 5 for:",
            "",
            "- strategic fit",
            "- distinctiveness",
            "- trustworthiness",
            "- memorability",
            "- avoidance of known bad patterns",
            "",
            "Use the founder profile, required qualities, forbidden terms, and "
            "evaluation notes as the source of truth.",
            "",
            "## Cases",
            "",
        ]

        answer_key = []
        for index, case_report in enumerate(data.get("cases", []), start=1):
            lines.extend(
                cls._case_section(
                    index,
                    case_report,
                    benchmark_cases.get(case_report["case_id"]),
                )
            )
            answer_key.append(cls._answer_key_entry(index, case_report))

        lines.extend(
            [
                "## Answer key",
                "",
                "Do not read this section until after scoring the candidate sets.",
                "",
            ]
        )
        lines.extend(answer_key)

        return "\n".join(lines).rstrip() + "\n"

    @classmethod
    def _case_section(
        cls,
        index: int,
        case_report: dict[str, Any],
        benchmark_case: Any | None,
    ) -> list[str]:
        case_id = case_report["case_id"]
        active = case_report["naming_output"]
        shadow = case_report.get("intent_shadow_naming_output")
        set_a = active
        set_b = shadow or {
            "candidates": [],
            "selected_name": "",
            "reasoning": "No intent-shadow naming output was produced.",
        }

        return [
            f"### Case {index}: {case_id}",
            "",
            *cls._case_context_lines(benchmark_case),
            f"- Forbidden term violations: "
            f"{_format_violations(case_report['naming_metrics'])}",
            f"- Intent-shadow overlap with active: "
            f"{len(case_report.get('intent_shadow_name_overlap', []))}",
            "",
            "#### Candidate Set A",
            "",
            *_candidate_lines(set_a),
            "",
            "Reviewer notes:",
            "",
            "- Strategic fit:",
            "- Distinctiveness:",
            "- Trustworthiness:",
            "- Memorability:",
            "- Known bad pattern risk:",
            "- Preferred name:",
            "",
            "#### Candidate Set B",
            "",
            *_candidate_lines(set_b),
            "",
            "Reviewer notes:",
            "",
            "- Strategic fit:",
            "- Distinctiveness:",
            "- Trustworthiness:",
            "- Memorability:",
            "- Known bad pattern risk:",
            "- Preferred name:",
            "",
        ]

    @staticmethod
    def _case_context_lines(benchmark_case: Any | None) -> list[str]:
        if benchmark_case is None:
            return []

        profile = benchmark_case.profile
        return [
            "Founder profile:",
            "",
            f"- Problem: {profile.problem}",
            f"- Audience: {profile.audience}",
            f"- Vision: {profile.vision}",
            f"- Principles: {profile.principles}",
            f"- Differentiation: {profile.differentiation}",
            "",
            "Evaluation constraints:",
            "",
            f"- Required qualities: {', '.join(benchmark_case.required_qualities)}",
            f"- Forbidden terms: {', '.join(benchmark_case.forbidden_terms)}",
            f"- Known bad patterns: {', '.join(benchmark_case.known_bad_patterns)}",
            f"- Notes: {benchmark_case.evaluation_notes}",
            "",
        ]

    @staticmethod
    def _answer_key_entry(
        index: int,
        case_report: dict[str, Any],
    ) -> str:
        shadow = case_report.get("intent_shadow_naming_output")
        shadow_approach = shadow["approach"] if shadow else "none"
        return (
            f"- Case {index} `{case_report['case_id']}`: "
            f"Set A = `{case_report['naming_output']['approach']}`, "
            f"Set B = `{shadow_approach}`"
        )


def _candidate_lines(output: dict[str, Any]) -> list[str]:
    candidates = output.get("candidates", [])
    if not candidates:
        return ["No candidates."]
    return [
        f"{index}. {candidate}"
        for index, candidate in enumerate(candidates, start=1)
    ]


def _format_violations(metrics: dict[str, Any]) -> str:
    violations = metrics.get("forbidden_term_violations", [])
    if not violations:
        return "none"
    return ", ".join(violations)
