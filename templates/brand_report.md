# Brand Strategy Report

## Executive Summary

{{ report.executive_summary }}

## Founder Insights

{{ report.founder_insights }}

## Brand Identity

{{ report.brand_identity }}

## Mission Statement

{{ report.mission_statement }}

## Vision Statement

{{ report.vision_statement }}

## Core Values

{{ report.core_values }}

## Positioning

{{ report.positioning }}

## Target Audience

{{ report.target_audience }}

## Brand Personality

{{ report.brand_personality }}

## Naming Strategy

{{ report.naming_strategy }}

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