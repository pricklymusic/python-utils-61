import collections
import functools
from typing import Any, Callable, Dict, List, Union

def munge(data: Any, path: str = '', sep: str = '.') -> Dict[str, Any]:
    """Flattens nested dicts into a dot-notated key map using recursion."""
    items = []
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{path}{sep}{k}" if path else k
            items.extend(munge(v, new_key, sep=sep).items())
    elif isinstance(data, list):
        for i, v in enumerate(data):
            items.extend(munge(v, f"{path}[{i}]", sep=sep).items())
    else:
        items.append((path, data))
    return dict(items)

def memo_with_expiry(ttl: int) -> Callable:
    """Decorator to cache function results with simple time-based expiry."""
    cache = {}
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            import time
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in cache:
                val, ts = cache[key]
                if now - ts < ttl:
                    return val
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

def smart_cast(value: str) -> Union[int, float, bool, str]:
    """Attempts to coerce string data to primitive types."""
    val = value.lower()
    if val in ('true', 'false'): return val == 'true'
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value