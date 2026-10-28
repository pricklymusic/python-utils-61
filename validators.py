import re
from typing import Any, Callable, Dict

def validate_schema(data: Dict[str, Any], schema: Dict[str, Callable[[Any], bool]]) -> bool:
    """Checks dict structure against a map of validator functions."""
    return all(key in data and validator(data[key]) for key, validator in schema.items())

def is_email(value: Any) -> bool:
    """Regex check for basic email pattern existence."""
    if not isinstance(value, str): return False
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", value))

def is_non_empty_str(value: Any) -> bool:
    """Identity check for non-empty string types."""
    return isinstance(value, str) and len(value.strip()) > 0

def compose_validators(*funcs: Callable[[Any], bool]) -> Callable[[Any], bool]:
    """Functional composition of validation predicates."""
    return lambda x: all(f(x) for f in funcs)

def range_check(min_val: float, max_val: float) -> Callable[[Any], bool]:
    """Closure generator for range-based validation."""
    def check(val: Any) -> bool:
        try:
            return min_val <= float(val) <= max_val
        except (ValueError, TypeError):
            return False
    return check