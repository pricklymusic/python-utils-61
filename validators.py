import re
from typing import Any, Optional

def is_email(value: Any) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return isinstance(value, str) and bool(re.match(pattern, value))

def is_safe_identifier(value: Any) -> bool:
    return isinstance(value, str) and value.isidentifier()

def strict_cast(value: Any, target_type: type, default: Any = None) -> Any:
    try:
        if not isinstance(value, target_type):
            return target_type(value)
        return value
    except (ValueError, TypeError):
        return default

def batch_validate(items: list, validator: callable) -> list:
    return [item for item in items if validator(item)]

def validate_schema(data: dict, schema: dict) -> bool:
    for key, expected_type in schema.items():
        if key not in data or not isinstance(data[key], expected_type):
            return False
    return True

class Guard:
    def __init__(self, value: Any):
        self.value = value
    
    def ensure(self, predicate: callable, error_msg: str = "validation failed"):
        if not predicate(self.value):
            raise ValueError(error_msg)
        return self