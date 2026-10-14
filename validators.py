from typing import Any, Callable, Dict, List, Optional

class ValidatorRegistry:
    def __init__(self) -> None:
        self._rules: Dict[str, List[Callable[[Any], bool]]] = {}

    def register(self, key: str, func: Callable[[Any], bool]) -> None:
        if key not in self._rules:
            self._rules[key] = []
        self._rules[key].append(func)

    def validate(self, key: str, value: Any) -> bool:
        rules = self._rules.get(key, [])
        return all(rule(value) for rule in rules) if rules else True

    def __call__(self, key: str) -> Callable[[Callable[[Any], bool]], Callable[[Any], bool]]:
        def decorator(func: Callable[[Any], bool]) -> Callable[[Any], bool]:
            self.register(key, func)
            return func
        return decorator

validate_engine = ValidatorRegistry()

@validate_engine('email')
def _is_email(val: Any) -> bool:
    return isinstance(val, str) and '@' in val and '.' in val

@validate_engine('non_empty')
def _is_non_empty(val: Any) -> bool:
    return bool(val) and len(str(val)) > 0

def check_structure(data: Dict[str, Any], schema: Dict[str, str]) -> bool:
    for key, rule_name in schema.items():
        if not validate_engine.validate(rule_name, data.get(key)):
            return False
    return True