"""
Project Origin - Data Models

This module defines structured data used by Project Origin.
"""

from dataclasses import dataclass, asdict
import json


@dataclass
class FounderProfile:
    problem: str
    audience: str
    vision: str
    principles: str
    differentiation: str

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)