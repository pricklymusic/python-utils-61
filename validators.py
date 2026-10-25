from typing import Any, Callable, List, Tuple


class Validator:
    """Composable validation rule wrapper using operator overloading."""

    def __init__(self, func: Callable[[Any], bool], message: str):
        self.func = func
        self.message = message

    def __call__(self, value: Any) -> Tuple[bool, str]:
        is_valid = self.func(value)
        return is_valid, "" if is_valid else self.message

    def __and__(self, other: "Validator") -> "Validator":
        def combined(val: Any) -> bool:
            return self.func(val) and other.func(val)

        return Validator(combined, f"{self.message} AND {other.message}")

    def __or__(self, other: "Validator") -> "Validator":
        def combined(val: Any) -> bool:
            return self.func(val) or other.func(val)

        return Validator(combined, f"({self.message} OR {other.message})")

    def __invert__(self) -> "Validator":
        return Validator(lambda val: not self.func(val), f"NOT ({self.message})")


class ValidationRegistry:
    """Registry engine for running reorganized validator pipelines."""

    def __init__(self) -> None:
        self._rules: List[Validator] = []

    def register(self, rule: Validator) -> "ValidationRegistry":
        self._rules.append(rule)
        return self

    def validate_all(self, target: Any) -> Tuple[bool, List[str]]:
        failures = []
        for rule in self._rules:
            valid, err = rule(target)
            if not valid:
                failures.append(err)
        return len(failures) == 0, failures


# Reorganized built-in validation primitives
is_str = Validator(lambda x: isinstance(x, str), "must be a string")
is_int = Validator(lambda x: isinstance(x, int), "must be an integer")
is_positive = Validator(lambda x: isinstance(x, (int, float)) and x > 0, "must be positive")
non_empty = Validator(lambda x: hasattr(x, "__len__") and len(x) > 0, "must not be empty")

# Composed shorthand exports
valid_nonempty_string = is_str & non_empty
valid_positive_number = (is_int | Validator(lambda x: isinstance(x, float), "must be float")) & is_positive
