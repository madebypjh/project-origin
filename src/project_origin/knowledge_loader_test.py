from src.project_origin.naming.knowledge_loader import NamingKnowledgeLoader


def main():
    knowledge = NamingKnowledgeLoader.load()

    print("===== NAMING KNOWLEDGE =====")
    print(knowledge)


if __name__ == "__main__":
    main()