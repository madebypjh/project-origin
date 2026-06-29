"""
Project Origin - Brand Application Layer

Coordinates the full application workflow.
"""

import os

from project_origin.brand.decision import NamingDecisionService
from project_origin.brand.file_writer import FileWriter
from project_origin.brand.interview import InterviewSession
from project_origin.brand.knowledge_builder import KnowledgeBuilder
from project_origin.brand.language_engine import BrandLanguageEngine
from project_origin.brand.markdown_report import MarkdownReportGenerator
from project_origin.brand.naming.evaluator import NameEvaluator
from project_origin.brand.naming.filters import NameFilterPipeline
from project_origin.brand.naming.generator import NamingGenerator
from project_origin.brand.naming.ranker import NameRanker
from project_origin.brand.prompt_builder import PromptBuilder
from project_origin.brand.report_parser import ReportParser
from project_origin.brand.semantic.semantic_engine import SemanticEngine
from project_origin.llm.base import LLMProvider
from project_origin.llm.factory import LLMFactory


DEBUG = False


class BrandApplication:
    def __init__(self, provider: LLMProvider | None = None) -> None:
        provider_name = os.getenv("PROJECT_ORIGIN_LLM_PROVIDER", "openai")
        self.provider = provider or LLMFactory.create(provider_name)

    def run(self) -> None:
        profile = self._run_interview()

        if DEBUG:
            self._print_structured_profile(profile)

        knowledge = self._build_knowledge(profile)

        if DEBUG:
            self._print_brand_knowledge(knowledge)

        decision = self._build_naming_decision(profile, knowledge)
        FileWriter.save_naming_decision(decision)
        prompt = PromptBuilder.build(profile, knowledge, decision.result)

        if DEBUG:
            self._print_prompt(prompt)

        raw_response = self._generate_llm_response(prompt)
        report = self._parse_report(raw_response, decision.result)
        markdown = self._generate_markdown(report)

        self._print_markdown_report(markdown)

        file_path = FileWriter.save_markdown(markdown)
        self._print_saved_file(file_path)

    def _run_interview(self):
        session = InterviewSession()
        return session.run()

    def _build_knowledge(self, profile):
        return KnowledgeBuilder.build(profile)

    def _build_naming_decision(self, profile, knowledge):
        semantic_profile = SemanticEngine.build(profile)
        brand_language = BrandLanguageEngine.build(semantic_profile)

        names = NamingGenerator.generate(brand_language, count=100)
        filtered_names = NameFilterPipeline.apply(names)
        evaluated_names = NameEvaluator.evaluate(filtered_names, brand_language)
        ranked_names = NameRanker.rank(evaluated_names, limit=20)
        FileWriter.save_name_candidates(ranked_names)

        return NamingDecisionService.decide(
            profile=profile,
            knowledge=knowledge,
            candidates=ranked_names,
        )

    def _generate_llm_response(self, prompt: str) -> str:
        return self.provider.generate(prompt)

    def _parse_report(self, raw_response: str, decision):
        return ReportParser.parse(raw_response, decision)

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
