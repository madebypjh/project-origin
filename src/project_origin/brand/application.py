"""
Project Origin - Brand Application Layer

Coordinates the full application workflow.
"""

import os

from project_origin.brand.decision import NamingDecisionService
from project_origin.brand.file_writer import FileWriter
from project_origin.brand.interview import InterviewSession
from project_origin.brand.intent import (
    BrandLanguageFromIntent,
    BrandIntentShadowService,
    LlmBrandIntentInterpreter,
)
from project_origin.brand.intent.models import BrandIntentShadowRecord
from project_origin.brand.knowledge_builder import KnowledgeBuilder
from project_origin.brand.language_engine import BrandLanguageEngine
from project_origin.brand.markdown_report import MarkdownReportGenerator
from project_origin.brand.naming.evaluator import NameEvaluator
from project_origin.brand.naming.filters import NameFilterPipeline
from project_origin.brand.naming.generation_rules import GenerationRulesBuilder
from project_origin.brand.naming.generator import NamingGenerator
from project_origin.brand.naming.knowledge_loader import NamingKnowledgeLoader
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

        intent_record = self._run_intent_shadow(profile)
        knowledge = self._build_knowledge(profile)

        if DEBUG:
            self._print_brand_knowledge(knowledge)

        decision = self._build_naming_decision(
            profile,
            knowledge,
            intent_record=intent_record,
        )
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

    def _run_intent_shadow(self, profile) -> BrandIntentShadowRecord | None:
        if not self._intent_shadow_enabled():
            return None

        record = self._interpret_intent_shadow(profile)
        FileWriter.save_intent_shadow(record)
        return record

    @staticmethod
    def _intent_shadow_enabled() -> bool:
        value = os.getenv("PROJECT_ORIGIN_INTENT_SHADOW", "false")
        return value.strip().casefold() in {"1", "true", "yes", "on"}

    def _build_naming_decision(
        self,
        profile,
        knowledge,
        intent_record: BrandIntentShadowRecord | None = None,
    ):
        brand_language = self._build_brand_language(profile, intent_record)

        names = NamingGenerator.generate(brand_language, count=100)
        filtered_names = NameFilterPipeline.apply(names)
        evaluated_names = NameEvaluator.evaluate(
            filtered_names,
            brand_language,
            rules=self._build_generation_rules(),
        )
        ranked_names = NameRanker.rank(evaluated_names, limit=20)
        FileWriter.save_name_candidates(ranked_names)

        return NamingDecisionService.decide(
            profile=profile,
            knowledge=knowledge,
            candidates=ranked_names,
        )

    def _build_brand_language(
        self,
        profile,
        intent_record: BrandIntentShadowRecord | None = None,
    ):
        if self._intent_shadow_naming_enabled():
            record = intent_record or self._interpret_intent_shadow(profile)
            if intent_record is None:
                FileWriter.save_intent_shadow(record)
            if record.llm_candidate is not None:
                return BrandLanguageFromIntent.build(record.llm_candidate)

        semantic_profile = SemanticEngine.build(profile)
        return BrandLanguageEngine.build(semantic_profile)

    def _interpret_intent_shadow(self, profile) -> BrandIntentShadowRecord:
        service = BrandIntentShadowService(
            llm=LlmBrandIntentInterpreter(self.provider),
        )
        return service.interpret(profile)

    @staticmethod
    def _intent_shadow_naming_enabled() -> bool:
        value = os.getenv("PROJECT_ORIGIN_NAMING_PATH", "active")
        return value.strip().casefold() in {
            "intent_shadow",
            "intent-shadow",
            "b",
        }

    def _build_generation_rules(self):
        if not self._intent_shadow_naming_enabled():
            return None

        knowledge = NamingKnowledgeLoader.load()
        return GenerationRulesBuilder.build(knowledge)

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
