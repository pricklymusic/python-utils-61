from typing import Any, Callable, Dict, Optional

class Validator:
    """An unconventional validator factory for runtime type checking."""
    def __init__(self, check: Callable[[Any], bool], error_msg: str = "Validation failed") -> None:
        self.check = check
        self.error_msg = error_msg

    def __call__(self, value: Any) -> Any:
        if not self.check(value):
            raise ValueError(f"{self.error_msg}: {value}")
        return value

def validate_schema(data: Dict[str, Any], schema: Dict[str, Validator]) -> Dict[str, Any]:
    """Applies validators across a dictionary mapping."""
    return {k: v(data.get(k)) for k, v in schema.items()}

def is_int_range(low: int, high: int) -> Validator:
    """Creator for numeric range validators."""
    return Validator(
        lambda x: isinstance(x, int) and low <= x <= high,
        f"Value not in range [{low}, {high}]"
    )

def is_non_empty_str(value: Any) -> bool:
    """Checks if input is a non-empty string."""
    return isinstance(value, str) and len(value) > 0

string_validator: Validator = Validator(is_non_empty_str, "Empty string error")