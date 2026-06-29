"""
Project Origin - Application Layer

Coordinates the full application workflow.
"""

from .interview import InterviewSession
from .knowledge_builder import KnowledgeBuilder
from .prompt_builder import PromptBuilder
from .llm.factory import LLMFactory
from .report_parser import ReportParser
from .markdown_report import MarkdownReportGenerator
from .file_writer import FileWriter

from .semantic.semantic_engine import SemanticEngine
from .language_engine import BrandLanguageEngine
from .naming.generator import NamingGenerator
from .naming.evaluator import NameEvaluator
from .naming.ranker import NameRanker


DEBUG = False


class ProjectOriginApplication:
    def run(self) -> None:
        profile = self._run_interview()

        if DEBUG:
            self._print_structured_profile(profile)

        knowledge = self._build_knowledge(profile)

        if DEBUG:
            self._print_brand_knowledge(knowledge)

        prompt = self._build_prompt(profile)

        if DEBUG:
            self._print_prompt(prompt)

        raw_response = self._generate_llm_response(prompt)
        report = self._parse_report(raw_response)
        markdown = self._generate_markdown(report)

        self._print_markdown_report(markdown)

        file_path = FileWriter.save_markdown(markdown)
        self._print_saved_file(file_path)

    def _run_interview(self):
        session = InterviewSession()
        return session.run()

    def _build_knowledge(self, profile):
        return KnowledgeBuilder.build(profile)

    def _build_prompt(self, profile):
        semantic_profile = SemanticEngine.build(profile)
        brand_language = BrandLanguageEngine.build(semantic_profile)

        names = NamingGenerator.generate(brand_language, count=100)
        evaluated_names = NameEvaluator.evaluate(names, brand_language)
        ranked_names = NameRanker.rank(evaluated_names, limit=20)
        FileWriter.save_name_candidates(ranked_names)

        candidate_names = [candidate.name for candidate in ranked_names]

        return PromptBuilder.build(profile, candidate_names)

    def _generate_llm_response(self, prompt: str) -> str:
        provider = LLMFactory.create("openai")
        return provider.generate(prompt)

    def _parse_report(self, raw_response: str):
        return ReportParser.parse(raw_response)

    def _generate_markdown(self, report):
        return MarkdownReportGenerator.generate(report)

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

    def _print_markdown_report(self, markdown: str) -> None:
        print("\n==============================")
        print(" MARKDOWN REPORT ")
        print("==============================\n")
        print(markdown)

    def _print_saved_file(self, file_path) -> None:
        print("\n==============================")
        print(" REPORT SAVED ")
        print("==============================\n")
        print(f"Saved to: {file_path}")