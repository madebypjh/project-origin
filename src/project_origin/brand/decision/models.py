"""Brand-specific records that preserve complete Core decision context."""

from dataclasses import asdict, dataclass
import json

from project_origin.core import DecisionResult, IntentProfile, KnowledgePacket


@dataclass(frozen=True)
class BrandNamingDecisionEvidence:
    selected_name: str
    runner_up_name: str | None
    score_delta: float | None
    strategy_delta: float | None
    originality_delta: float | None
    memorability_delta: float | None
    selected_advantages: tuple[str, ...]
    runner_up_tradeoffs: tuple[str, ...]
    risk_assessment: tuple[str, ...]
    brand_history_seed: str
    brand_dna: tuple[str, ...]
    value_alignment: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class BrandNamingDecisionRecord:
    intent: IntentProfile
    knowledge: KnowledgePacket
    result: DecisionResult
    evidence: BrandNamingDecisionEvidence | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
