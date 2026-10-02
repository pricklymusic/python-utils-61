import math
from typing import Any, Callable, Dict, Optional, Tuple, Type


class SafeResult:
    def __init__(self, value: Any, error: Optional[BaseException] = None):
        self.value = value
        self.error = error
        self.is_ok = error is None

    def __bool__(self) -> bool:
        return self.is_ok

    def __repr__(self) -> str:
        status = "OK" if self.is_ok else f"ERR:{type(self.error).__name__}"
        return f"SafeResult({status}, value={self.value!r})"


def mitigate_edge_cases(
    fallback: Any = None,
    catches: Tuple[Type[BaseException], ...] = (Exception,),
) -> Callable:
    """Decorator intercepting unexpected edge cases and toxic input values."""

    def decorator(func: Callable[..., Any]) -> Callable[..., SafeResult]:
        def wrapper(*args: Any, **kwargs: Any) -> SafeResult:
            try:
                for arg in list(args) + list(kwargs.values()):
                    if isinstance(arg, float) and (math.isnan(arg) or math.isinf(arg)):
                        raise ArithmeticError(f"Non-finite float value encountered: {arg}")
                result = func(*args, **kwargs)
                return SafeResult(value=result)
            except catches as err:
                return SafeResult(value=fallback, error=err)

        return wrapper

    return decorator


class RobustSchemaValidator:
    def __init__(self, rules: Dict[str, Callable[[Any], bool]]):
        self.rules = rules

    def validate_field(self, field_name: str, value: Any) -> SafeResult:
        if field_name not in self.rules:
            return SafeResult(value=False, error=KeyError(f"No rule for field '{field_name}'"))

        guarded_rule = mitigate_edge_cases(fallback=False)(self.rules[field_name])
        return guarded_rule(value)

    def validate_payload(self, payload: Dict[str, Any]) -> Dict[str, SafeResult]:
        results = {}
        for field_name, rule in self.rules.items():
            val = payload.get(field_name)
            results[field_name] = self.validate_field(field_name, val)
        return results
