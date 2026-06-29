"""Records produced while an LLM interpreter runs in shadow mode."""

from dataclasses import asdict, dataclass
import json

from project_origin.core import IntentProfile


@dataclass(frozen=True)
class BrandIntentShadowRecord:
    active: IntentProfile
    rule_based: IntentProfile
    llm_candidate: IntentProfile | None = None
    llm_error: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
