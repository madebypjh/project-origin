from benchmarks.brand_naming import BlindReviewMarkdownReport


def test_blind_review_markdown_hides_approaches_until_answer_key():
    report = {
        "cases": [
            {
                "case_id": "security-trust-platform",
                "naming_output": {
                    "approach": "project_origin",
                    "candidates": ["Alpha", "Beta"],
                    "selected_name": "Alpha",
                    "reasoning": "Active reasoning",
                },
                "naming_metrics": {
                    "forbidden_term_violations": [],
                },
                "intent_shadow_naming_output": {
                    "approach": "project_origin_intent_shadow_naming",
                    "candidates": ["Gamma", "Delta"],
                    "selected_name": "Gamma",
                    "reasoning": "Shadow reasoning",
                },
                "intent_shadow_name_overlap": [],
            }
        ]
    }

    markdown = BlindReviewMarkdownReport.from_report_data(report)
    case_section = markdown.split("## Answer key", 1)[0]
    answer_key = markdown.split("## Answer key", 1)[1]

    assert "# Brand Naming Blind Review" in markdown
    assert "Small security teams cannot prioritize" in case_section
    assert "Required qualities:" in case_section
    assert "Known bad patterns:" in case_section
    assert "Candidate Set A" in case_section
    assert "Candidate Set B" in case_section
    assert "1. Alpha" in case_section
    assert "1. Gamma" in case_section
    assert "project_origin" not in case_section
    assert "Set A = `project_origin`" in answer_key
    assert "Set B = `project_origin_intent_shadow_naming`" in answer_key
