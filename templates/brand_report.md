# Brand Strategy Report

## Executive Summary

{{ report.executive_summary }}

## Founder Insights

{{ report.founder_insights }}

## Brand Origin Story

{{ report.brand_origin_story }}

## Brand Identity

{{ report.brand_identity }}

## Brand DNA

{{ report.brand_dna }}

{% if report.brand_dna_items %}
| Principle | Meaning | How it shows up |
| --- | --- | --- |
{% for item in report.brand_dna_items -%}
| {{ item.principle }} | {{ item.meaning }} | {{ item.how_it_shows_up }} |
{% endfor %}
{% endif %}

## Mission Statement

{{ report.mission_statement }}

## Vision Statement

{{ report.vision_statement }}

## Core Values

{{ report.core_values }}

## Strategic Values

{{ report.strategic_values }}

{% if report.strategic_value_items %}
| Value | Strategic Role | Decision Rule |
| --- | --- | --- |
{% for item in report.strategic_value_items -%}
| {{ item.value }} | {{ item.strategic_role }} | {{ item.decision_rule }} |
{% endfor %}
{% endif %}

## Positioning

{{ report.positioning }}

## Target Audience

{{ report.target_audience }}

## Brand Personality

{{ report.brand_personality }}

## Naming Strategy

{{ report.naming_strategy }}

## Selected Name Rationale

{{ report.selected_name_rationale }}

## Candidate Comparison

{{ report.candidate_comparison }}

## Name Recommendations

{% for item in report.name_recommendations %}
### {{ item.name }}

- **Meaning:** {{ item.meaning }}
- **Strategic Fit:** {{ item.strategic_fit }}
- **Strengths:** {{ item.strengths }}
- **Weaknesses:** {{ item.weaknesses }}
- **Score:** {{ item.score }}/10
- **Reason:** {{ item.score_reason }}

{% endfor %}

## Final Recommendation

{{ report.final_recommendation }}

## Strategic Risks

{{ report.strategic_risks }}

## Next Action Plan

{{ report.next_action_plan }}
