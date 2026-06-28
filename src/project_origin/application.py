"""
Project Origin - Application Layer

Coordinates the full application workflow.
"""
DEBUG = False

from .interview import InterviewSession
from .knowledge_builder import KnowledgeBuilder
from .prompt_builder import PromptBuilder
from .llm.factory import LLMFactory
from .report_parser import ReportParser
from .markdown_report import MarkdownReportGenerator
from .file_writer import FileWriter

class ProjectOriginApplication:
    def run(self) -> None:
        profile = self._run_interview()
        if DEBUG:
            self._print_structured_profile(profile)

        knowledge = self._build_knowledge(profile)        

        prompt = self._build_prompt(profile)

        if DEBUG:
            self._print_prompt(prompt)

        raw_response = self._generate_llm_response(prompt)
        report = self._parse_report(raw_response)
        markdown = self._generate_markdown(report)
        file_path = FileWriter.save_markdown(markdown)
        self._print_saved_file(file_path)

        self._print_markdown_report(markdown)

    def _run_interview(self):
        session = InterviewSession()
        return session.run()

    def _build_knowledge(self, profile):
        return KnowledgeBuilder.build(profile)

    def _build_prompt(self, profile):
        return PromptBuilder.build(profile)

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