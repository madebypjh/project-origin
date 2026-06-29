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

## Mission Statement

{{ report.mission_statement }}

## Vision Statement

{{ report.vision_statement }}

## Core Values

{{ report.core_values }}

## Strategic Values

{{ report.strategic_values }}

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
