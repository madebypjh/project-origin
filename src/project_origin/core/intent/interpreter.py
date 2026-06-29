"""Provider-independent contract for interpreting raw domain input."""

from typing import Protocol, TypeVar

from project_origin.core.intent.models import IntentProfile


InputT = TypeVar("InputT", contravariant=True)


class IntentInterpreter(Protocol[InputT]):
    def interpret(self, input_data: InputT) -> IntentProfile:
        """Transform raw domain input into a validated IntentProfile."""
        ...
