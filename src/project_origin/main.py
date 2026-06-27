"""
Project Origin - Interview System v0.3
Bilingual interview + FounderProfile data model
"""

from models import FounderProfile


class InterviewSession:
    def __init__(self):
        self.questions = [
            {
                "key": "problem",
                "en": "What problem are you solving?",
                "kr": "당신은 어떤 문제를 해결하고 있나요?",
            },
            {
                "key": "audience",
                "en": "Who are you building for?",
                "kr": "누구를 위한 서비스를 만들고 있나요?",
            },
            {
                "key": "vision",
                "en": "What is your long-term vision?",
                "kr": "장기적인 비전은 무엇인가요?",
            },
            {
                "key": "principles",
                "en": "What principles will you never compromise?",
                "kr": "절대 타협하지 않을 원칙은 무엇인가요?",
            },
            {
                "key": "differentiation",
                "en": "Why is your solution different from others?",
                "kr": "당신의 솔루션이 다른 것들과 다른 이유는 무엇인가요?",
            },
        ]

    def run(self) -> FounderProfile:
        print("\n===================================")
        print(" Project Origin - Interview ")
        print("===================================\n")

        answers = {}

        for i, q in enumerate(self.questions, 1):
            print(f"Q{i}. {q['en']}")
            print(f"   ({q['kr']})")

            answer = input("A: ").strip()
            answers[q["key"]] = answer
            print()

        return FounderProfile(**answers)


def main():
    session = InterviewSession()
    profile = session.run()

    print("===================================")
    print(" Interview Complete ")
    print("===================================\n")

    print("===== STRUCTURED PROFILE =====\n")
    print(profile.to_json())


if __name__ == "__main__":
    main()