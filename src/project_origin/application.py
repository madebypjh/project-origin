"""
Project Origin - Application Layer

Coordinates the full application workflow.
"""

from .interview import InterviewSession
from .knowledge_builder import KnowledgeBuilder
from .prompt_builder import PromptBuilder


class ProjectOriginApplication:
    def run(self) -> None:
        profile = self._run_interview()
        self._print_structured_profile(profile)

        knowledge = self._build_knowledge(profile)
        self._print_brand_knowledge(knowledge)

        prompt = self._build_prompt(profile)
        self._print_prompt(prompt)

    def _run_interview(self):
        session = InterviewSession()
        return session.run()

    def _build_knowledge(self, profile):
        return KnowledgeBuilder.build(profile)

    def _build_prompt(self, profile):
        return PromptBuilder.build(profile)

    def _print_structured_profile(self, profile) -> None:
        print("===================================")
        print(" Interview Complete ")
        print("===================================\n")

        print("===== STRUCTURED PROFILE =====\n")
        print(profile.to_json())

    def _print_brand_knowledge(self, knowledge) -> None:
        print("\n===== BRAND KNOWLEDGE =====\n")
        print(knowledge.to_json())

    def _print_prompt(self, prompt: str) -> None:
        print("\n==============================")
        print(" GENERATED PROMPT ")
        print("==============================\n")
        print(prompt)