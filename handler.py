from typing import Any, Callable, Dict, List, Union
from functools import wraps

def pipeline(data: Any, *funcs: Callable) -> Any:
    """Chain data through a sequence of callables."""
    for func in funcs:
        data = func(data)
    return data

def robust_fetch(container: Union[Dict, List], path: str, default: Any = None) -> Any:
    """Access nested data using dot notation strings."""
    keys = path.split('.')
    try:
        for key in keys:
            if isinstance(container, list):
                container = container[int(key)]
            else:
                container = container[key]
        return container
    except (KeyError, IndexError, ValueError, TypeError):
        return default

def memoize_once(func: Callable) -> Callable:
    """Cache result of function execution once."""
    cache = {}
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

class DataSanitizer:
    """Fluently strip unwanted values from structures."""
    def __init__(self, target: Any):
        self.target = target

    def purge(self, skip_values: List[Any] = [None, ""]):
        if isinstance(self.target, dict):
            self.target = {k: v for k, v in self.target.items() if v not in skip_values}
        elif isinstance(self.target, list):
            self.target = [v for v in self.target if v not in skip_values]
        return self