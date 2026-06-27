"""
Project Origin - Main Orchestrator
"""

from .interview import InterviewSession
from .knowledge_builder import KnowledgeBuilder
from .prompt_builder import PromptBuilder


def main():
    session = InterviewSession()
    profile = session.run()

    print("===================================")
    print(" Interview Complete ")
    print("===================================\n")

    print("===== STRUCTURED PROFILE =====\n")
    print(profile.to_json())

    knowledge = KnowledgeBuilder.build(profile)

    print("\n===== BRAND KNOWLEDGE =====\n")
    print(knowledge.to_json())

    prompt = PromptBuilder.build(profile)

    print("\n==============================")
    print(" GENERATED PROMPT ")
    print("==============================\n")
    print(prompt)


if __name__ == "__main__":
    main()