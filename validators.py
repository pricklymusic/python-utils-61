import re
from typing import Any, Callable


class Validator:
    """Composable validator with bitwise logic support."""

    def __init__(self, predicate: Callable[[Any], bool], message: str = "Validation failed"):
        self.predicate = predicate
        self.message = message

    def __call__(self, value: Any) -> bool:
        try:
            return bool(self.predicate(value))
        except (TypeError, ValueError):
            return False

    def __and__(self, other: "Validator") -> "Validator":
        return Validator(
            lambda v: self(v) and other(v),
            f"({self.message} AND {other.message})",
        )

    def __or__(self, other: "Validator") -> "Validator":
        return Validator(
            lambda v: self(v) or other(v),
            f"({self.message} OR {other.message})",
        )

    def __invert__(self) -> "Validator":
        return Validator(lambda v: not self(v), f"NOT ({self.message})")

    def check(self, value: Any) -> tuple[bool, str]:
        ok = self(value)
        return ok, "" if ok else f"Validation failed: {self.message}"

    def enforce(self, value: Any) -> Any:
        ok, err = self.check(value)
        if not ok:
            raise ValueError(err)
        return value


def is_type(expected_type: type) -> Validator:
    return Validator(lambda v: isinstance(v, expected_type), f"is instance of {expected_type.__name__}")


def matches(pattern: str) -> Validator:
    rx = re.compile(pattern)
    return Validator(lambda v: isinstance(v, str) and bool(rx.search(v)), f"matches pattern {pattern}")


def in_range(min_val: float, max_val: float) -> Validator:
    return Validator(lambda v: min_val <= v <= max_val, f"value in range [{min_val}, {max_val}]")


def is_email() -> Validator:
    return matches(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
