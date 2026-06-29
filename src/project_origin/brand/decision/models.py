"""Brand-specific records that preserve complete Core decision context."""

from dataclasses import asdict, dataclass
import json

from project_origin.core import DecisionResult, IntentProfile, KnowledgePacket


@dataclass(frozen=True)
class BrandNamingDecisionRecord:
    intent: IntentProfile
    knowledge: KnowledgePacket
    result: DecisionResult

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
