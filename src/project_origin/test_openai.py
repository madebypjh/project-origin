from .llm.openai_provider import OpenAIProvider

provider = OpenAIProvider()

response = provider.generate("Say hello in Korean.")

print(response)