from src.project_origin.naming.knowledge_loader import NamingKnowledgeLoader
from src.project_origin.naming.generation_rules import GenerationRulesBuilder


def main():
    knowledge = NamingKnowledgeLoader.load()
    rules = GenerationRulesBuilder.build(knowledge)

    print("===== GENERATION RULES =====")
    print(rules.to_json())


if __name__ == "__main__":
    main()