from typing import Any, Callable, Dict

class DataValidator:
    """A registry-based approach for arbitrary data validation."""
    _registry: Dict[str, Callable[[Any], bool]] = {}

    @classmethod
    def register(cls, name: str):
        def wrapper(func: Callable[[Any], bool]):
            cls._registry[name] = func
            return func
        return wrapper

    @classmethod
    def validate(cls, name: str, value: Any) -> bool:
        validator = cls._registry.get(name)
        if not validator:
            raise ValueError(f"No validator found for: {name}")
        return validator(value)

def validator_factory(check: Callable[[Any], bool]):
    """Functional wrapper for inline validation logic."""
    return lambda x: check(x)

@DataValidator.register("positive")
def _is_positive(val: Any) -> bool:
    return isinstance(val, (int, float)) and val > 0

@DataValidator.register("non_empty")
def _is_non_empty(val: Any) -> bool:
    return bool(val) if hasattr(val, '__len__') else False

class SchemaNode:
    def __init__(self, key: str, validator_name: str):
        self.key = key
        self.validator_name = validator_name

    def check(self, data: dict) -> bool:
        return DataValidator.validate(self.validator_name, data.get(self.key))