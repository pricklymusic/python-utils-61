from typing import Any, Callable, Dict, List, Optional

class DataValidator:
    """Chainable validator using functional dispatching."""
    def __init__(self, data: Any):
        self.data = data
        self._errors: List[str] = []

    def check(self, predicate: Callable[[Any], bool], message: str) -> 'DataValidator':
        if not predicate(self.data):
            self._errors.append(message)
        return self

    def validate(self) -> bool:
        return len(self._errors) == 0

    @property
    def errors(self) -> List[str]:
        return self._errors

def schema_enforce(schema: Dict[str, Callable[[Any], bool]]):
    """Decorator for dictionary integrity verification."""
    def decorator(func):
        def wrapper(data: Dict[str, Any], *args, **kwargs):
            for key, validator in schema.items():
                if key not in data or not validator(data[key]):
                    raise ValueError(f"Invalid data at field: {key}")
            return func(data, *args, **kwargs)
        return wrapper
    return decorator

# Helper predicates
is_not_empty = lambda x: x is not None and len(str(x)) > 0
is_numeric = lambda x: isinstance(x, (int, float))
is_email = lambda x: isinstance(x, str) and "@" in x