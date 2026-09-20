import re
from typing import Any, Callable, Dict

def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def satisfies_all(obj: Any, predicates: Dict[str, Callable[[Any], bool]]) -> bool:
    return all(predicate(obj) for predicate in predicates.values())

def enforce_types(schema: Dict[str, type]) -> Callable:
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            params = {**dict(zip(func.__code__.co_varnames, args)), **kwargs}
            for name, expected_type in schema.items():
                if name in params and not isinstance(params[name], expected_type):
                    raise TypeError(f'argument {name} must be {expected_type.__name__}')
            return func(*args, **kwargs)
        return wrapper
    return decorator

def sanitize_input(value: Any) -> str:
    if not isinstance(value, str):
        return str(value)
    return ''.join(c for c in value if c.isalnum() or c in ' ._-')