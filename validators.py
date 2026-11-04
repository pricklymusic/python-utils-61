from typing import Any, Callable, Generator, Iterable

class ValidationRule:
    def __init__(self, predicate: Callable[[Any], bool], message: str):
        self.predicate = predicate
        self.message = message

    def __and__(self, other: "ValidationRule") -> "ValidationRule":
        return ValidationRule(
            lambda x: self.predicate(x) and other.predicate(x),
            f"{self.message} & {other.message}"
        )

    def __call__(self, value: Any) -> bool:
        return self.predicate(value)

def is_type(target_type: type) -> ValidationRule:
    return ValidationRule(
        lambda x: isinstance(x, target_type),
        f"type=={target_type.__name__}"
    )

def in_range(low: float, high: float) -> ValidationRule:
    return ValidationRule(
        lambda x: isinstance(x, (int, float)) and low <= x <= high,
        f"{low}<=val<={high}"
    )

def validate_and_process(
    source: Iterable[Any],
    rule: ValidationRule,
    processor: Callable[[Any], Any],
    on_error: Callable[[Any, str], Any] | None = None
) -> Generator[Any, None, None]:
    """Main processing loop validating inputs against composed rules."""
    for item in source:
        if rule(item):
            yield processor(item)
        elif on_error:
            yield on_error(item, f"Failed rule: {rule.message}")
