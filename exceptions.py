import sys
from typing import Any, Callable


class ProcessingError(Exception):
    """Base exception for processing failures with custom payloads."""

    def __init__(self, message: str, payload: Any = None) -> None:
        self.payload = payload
        super().__init__(f"{message} [offending_payload={payload!r}]")


class InvalidInputError(ProcessingError):
    """Raised when runtime inputs violate validation bounds."""


class input_validator:
    """A scope-level validator implemented as a context manager.

    Validates any newly introduced or modified variables within its block.
    """

    def __init__(
        self, predicate: Callable[[Any], bool], error_msg: str = "Invalid value"
    ) -> None:
        self.predicate = predicate
        self.error_msg = error_msg
        self._captured_locals: dict[str, Any] = {}

    def __enter__(self) -> "input_validator":
        # Retrieve parent frame's local variables upon entry
        frame = sys._getframe(1)
        self._captured_locals = dict(frame.f_locals)
        return self

    def __exit__(self, exc_type: Any, exc_val