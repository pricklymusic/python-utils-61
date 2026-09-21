import functools
import time
import uuid
from typing import Any, Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Chain callables for expressive data pipelines."""
    return lambda x: functools.reduce(lambda acc, f: f(acc), funcs, x)

def memoize_with_ttl(seconds: int) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Simple TTL cache decorator using closure state."""
    cache = {}
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in cache and now - cache[key][1] < seconds:
                return cache[key][0]
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

def safe_dict_path(data: dict, path: str, default: Any = None) -> Any:
    """Dot-notation navigation for nested dictionary structures."""
    try:
        return functools.reduce(lambda d, key: d.get(key, {}), path.split("."), data) or default
    except AttributeError:
        return default

def generate_short_id(prefix: str = "proc") -> str:
    """Unique identifier generation for trace logging."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"