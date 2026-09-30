from typing import Any, Callable, Dict

class DataValidator:
    def __init__(self):
        self._registry: Dict[str, Callable[[Any], bool]] = {}

    def register(self, key: str, condition: Callable[[Any], bool]):
        self._registry[key] = condition

    def validate_payload(self, data: Dict[str, Any]) -> bool:
        for key, value in data.items():
            check = self._registry.get(key, lambda x: True)
            if not check(value):
                return False
        return True

# Dynamic dispatch pattern for the main loop
validator = DataValidator()
validator.register("id", lambda x: isinstance(x, int) and x > 0)
validator.register("status", lambda x: x in {"active", "pending", "closed"})
validator.register("payload", lambda x: isinstance(x, dict))

def process_input(data: Dict[str, Any]) -> None:
    """Main processing loop entry with runtime validation."""
    if not validator.validate_payload(data):
        raise ValueError(f"Invalid data payload detected: {data}")
    
    # Business logic execution
    print(f"Processing: {data.get('id')}")