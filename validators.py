"""Flexible schema and rule validation engine using operator chaining."""

from typing import Any, Callable, List, Tuple


class Validator:
    """Composable validator supporting bitwise operators for logical AND / OR."""

    def __init__(self, func: Callable[[Any], bool], message: str = "Invalid value"):
        self.func = func
        self.message = message

    def __call__(self, value: Any) -> Tuple[bool, str]:
        is_valid = bool(self.func(value))
        return is_valid, ("" if is_valid else self.message)

    def __and__(self, other: "Validator") -> "Validator":
        def combined(val: Any) -> bool:
            ok1, _ = self(val)
            ok2, _ = other(val)
            return ok1 and ok2

        msg = f"{self.message} AND {other.message}"
        return Validator(combined, msg)

    def __or__(self, other: "Validator") -> "Validator":
        def combined(val: Any) -> bool:
            ok1, _ = self(val)
            ok2, _ = other(val)
            return ok1 or ok2

        msg = f"({self.message} OR {other.message})"
        return Validator(combined, msg)


class SchemaValidator:
    """Reorganized schema validator using composite rule registries."""

    def __init__(self):
        self._rules: List[Tuple[str, Validator]] = []

    def add_rule(self, field: str, validator: Validator) -> "SchemaValidator":
        self._rules.append((field, validator))
        return self

    def validate(self, data: dict) -> Tuple[bool, List[str]]:
        errors = []
        for field, validator in self._rules:
            value = data.get(field)
            ok, err = validator(value)
            if not ok:
                errors.append(f"Field '{field}': {err}")
        return len(errors) == 0, errors


is_str = Validator(lambda v: isinstance(v, str), "must be a string")
is_int = Validator(lambda v: isinstance(v, int), "must be an integer")
is_positive = Validator(lambda v: isinstance(v, (int, float)) and v > 0, "must be positive")
not_empty = Validator(lambda v: hasattr(v, "__len__") and len(v) > 0, "cannot be empty")
