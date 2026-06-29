from project_origin.brand.application import BrandApplication
from project_origin.brand.file_writer import FileWriter
from project_origin.brand.knowledge_builder import KnowledgeBuilder
from project_origin.brand.models import FounderProfile
from project_origin.llm.mock_provider import MockProvider


def _profile() -> FounderProfile:
    return FounderProfile(
        problem="Founders cannot explain complex decisions clearly.",
        audience="startup founders",
        vision="Make strategic reasoning understandable.",
        principles="Truth, evidence, and clarity",
        differentiation="Turns messy reasoning into explainable choices.",
    )


def _disable_file_writes(monkeypatch) -> None:
    monkeypatch.setattr(
        FileWriter,
        "save_name_candidates",
        staticmethod(lambda candidates: None),
    )
    monkeypatch.setattr(
        FileWriter,
        "save_intent_shadow",
        staticmethod(lambda record: None),
    )


def test_application_uses_active_naming_path_by_default(monkeypatch):
    _disable_file_writes(monkeypatch)
    monkeypatch.delenv("PROJECT_ORIGIN_NAMING_PATH", raising=False)
    app = BrandApplication(provider=MockProvider())
    profile = _profile()
    knowledge = KnowledgeBuilder.build(profile)

    decision = app._build_naming_decision(profile, knowledge)
    semantic_directions = [
        option.metadata["semantic_direction"]
        for option in decision.result.options
    ]

    assert all(
        "interpreted intent signals" not in direction
        for direction in semantic_directions
    )


def test_application_can_use_intent_shadow_naming_path(monkeypatch):
    _disable_file_writes(monkeypatch)
    monkeypatch.setenv("PROJECT_ORIGIN_NAMING_PATH", "intent_shadow")
    app = BrandApplication(provider=MockProvider())
    profile = _profile()
    knowledge = KnowledgeBuilder.build(profile)

    decision = app._build_naming_decision(profile, knowledge)
    semantic_directions = [
        option.metadata["semantic_direction"]
        for option in decision.result.options
    ]

    assert all(
        "interpreted intent signals" in direction
        for direction in semantic_directions
    )
    assert len(decision.result.options) == 20
