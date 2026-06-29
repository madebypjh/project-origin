import json

from project_origin.brand.intent import (
    BrandLanguageFromIntent,
    BrandIntentShadowService,
    LlmBrandIntentInterpreter,
    RuleBasedBrandIntentInterpreter,
)
from project_origin.brand.intent.policy import BrandIntentPolicy
from project_origin.brand.models import FounderProfile
from project_origin.brand.semantic.theme_detector import ThemeDetector
from project_origin.llm.mock_provider import MockProvider


class StaticProvider:
    def __init__(self, response: dict) -> None:
        self.response = response

    def generate(self, prompt: str) -> str:
        return json.dumps(self.response)


def _health_profile() -> FounderProfile:
    return FounderProfile(
        problem="People cannot turn daily health signals into sustainable habits.",
        audience="health-conscious adults",
        vision="Make preventive health guidance understandable and humane.",
        principles="Privacy, empathy, and medical humility",
        differentiation="Explain patterns without pretending to replace clinicians.",
    )


def test_llm_interpreter_accepts_open_ended_grounded_concepts():
    provider = StaticProvider(
        {
            "signals": [
                {
                    "kind": "value",
                    "concept": "medical humility",
                    "weight": 0.6,
                    "evidence": ["medical humility"],
                    "confidence": 0.95,
                },
                {
                    "kind": "desired_emotion",
                    "concept": "humane guidance",
                    "weight": 0.4,
                    "evidence": ["understandable and humane"],
                    "confidence": 0.85,
                },
            ],
            "unresolved_signals": [],
        }
    )

    intent = LlmBrandIntentInterpreter(provider).interpret(_health_profile())

    assert [signal.concept for signal in intent.signals] == [
        "medical_humility",
        "humane_guidance",
    ]
    assert sum(signal.weight for signal in intent.signals) == 1.0


def test_llm_interpreter_rejects_hallucinated_evidence():
    provider = StaticProvider(
        {
            "signals": [
                {
                    "kind": "value",
                    "concept": "luxury",
                    "weight": 1.0,
                    "evidence": ["premium luxury experience"],
                    "confidence": 0.9,
                }
            ],
            "unresolved_signals": [],
        }
    )

    record = BrandIntentShadowService(
        llm=LlmBrandIntentInterpreter(provider),
    ).interpret(_health_profile())

    assert record.llm_candidate is None
    assert "not present" in record.llm_error
    assert record.active is record.rule_based


def test_rule_based_interpreter_does_not_match_ai_inside_words():
    profile = FounderProfile(
        problem="Help people maintain sustainable habits.",
        audience="local communities",
        vision="Build a durable service.",
        principles="Care and patience",
        differentiation="Human guidance",
    )

    intent = RuleBasedBrandIntentInterpreter().interpret(profile)
    themes = ThemeDetector.detect(profile)

    assert "technology" not in themes
    assert all(signal.concept != "technology" for signal in intent.signals)


def test_mock_provider_supports_shadow_intent_interpretation():
    record = BrandIntentShadowService(
        llm=LlmBrandIntentInterpreter(MockProvider()),
    ).interpret(_health_profile())

    assert record.llm_error is None
    assert record.llm_candidate is not None
    assert len(record.llm_candidate.signals) == 4


def test_intent_policy_guides_llm_toward_stable_short_concepts():
    prompt = BrandIntentPolicy.build_prompt(_health_profile())

    assert "POLICY_VERSION: brand_intent_v2" in prompt
    assert "prefer 2 to 4 words" in prompt
    assert "name the reusable concept, not the full sentence" in prompt
    assert "trusted_decision_layer" in prompt
    assert "medical_humility" in prompt
    assert "non_clinician_replacement" in prompt


def test_intent_language_adapter_builds_brand_language_from_signals():
    record = BrandIntentShadowService(
        llm=LlmBrandIntentInterpreter(MockProvider()),
    ).interpret(_health_profile())

    language = BrandLanguageFromIntent.build(record.llm_candidate)

    assert language.vocabulary
    assert "problem" in language.vocabulary
    assert language.style in {"clear", "structured", "expressive"}
    assert "interpreted intent signals" in language.semantic_direction
