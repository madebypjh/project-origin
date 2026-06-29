"""System-neutral output format shared by all benchmark approaches."""

from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class BrandNamingBenchmarkOutput:
    case_id: str
    approach: str
    candidates: tuple[str, ...]
    selected_name: str
    reasoning: str
    latency_ms: float | None = None
    estimated_cost_usd: float | None = None

    def __post_init__(self) -> None:
        normalized = [name.casefold() for name in self.candidates]
        if not self.case_id.strip():
            raise ValueError("case_id must not be empty")
        if not self.approach.strip():
            raise ValueError("approach must not be empty")
        if not self.candidates:
            raise ValueError("candidates must not be empty")
        if len(normalized) != len(set(normalized)):
            raise ValueError("candidate names must be unique")
        if self.selected_name.casefold() not in normalized:
            raise ValueError("selected_name must reference one of candidates")
        if self.latency_ms is not None and self.latency_ms < 0:
            raise ValueError("latency_ms must be non-negative")
        if self.estimated_cost_usd is not None and self.estimated_cost_usd < 0:
            raise ValueError("estimated_cost_usd must be non-negative")

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
