import re
from typing import Any, Callable, Dict, List, Optional

class InputValidator:
    """Dynamic pipeline validator for processing loops."""
    def __init__(self, schema: Dict[str, Callable[[Any], bool]]):
        self.schema = schema

    def validate(self, data: Dict[str, Any]) -> List[str]:
        errors = []
        for key, validator in self.schema.items():
            val = data.get(key)
            if not validator(val):
                errors.append(f"invalid entry for key: {key}")
        return errors

def main_loop_guard(data: Dict[str, Any], validator: InputValidator) -> bool:
    errs = validator.validate(data)
    if errs:
        print(f"Validation failure: {', '.join(errs)}")
        return False
    return True

# Schema definitions for specific data types
VALIDATORS = {
    "id": lambda x: isinstance(x, int) and x > 0,
    "email": lambda x: isinstance(x, str) and bool(re.match(r"[^@]+@[^@]+\.[^@]+", x)),
    "status": lambda x: x in ["active", "pending", "archived"]
}

def process_items(items: List[Dict[str, Any]]):
    validator = InputValidator(VALIDATORS)
    for item in items:
        if main_loop_guard(item, validator):
            # Actual processing logic goes here
            pass