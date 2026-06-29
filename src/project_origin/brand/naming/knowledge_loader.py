"""
Project Origin - Naming Knowledge Loader

Loads compiled naming knowledge from the research pipeline.
"""

import json
from pathlib import Path


class NamingKnowledgeLoader:
    DEFAULT_PATH = Path("dataset") / "analysis" / "naming_knowledge.json"

    @classmethod
    def load(cls, industry: str | None = None) -> dict:
        knowledge_path = cls._get_project_root() / cls.DEFAULT_PATH

        if not knowledge_path.exists():
            return {}

        knowledge = json.loads(knowledge_path.read_text(encoding="utf-8"))

        if not industry:
            return knowledge.get("global", {})

        normalized_industry = industry.lower().strip()
        by_industry = knowledge.get("by_industry", {})

        return by_industry.get(
            normalized_industry,
            knowledge.get("global", {}),
        )

    @staticmethod
    def _get_project_root() -> Path:
        return Path(__file__).resolve().parents[4]
