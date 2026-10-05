import functools
from typing import Any, Callable, Dict

class DataPipe:
    """A fluent pipeline for data transformation using attribute injection."""
    def __init__(self, data: Any):
        self.data = data

    def __getattr__(self, name: str) -> Callable:
        def wrapper(*args, **kwargs):
            if hasattr(self.data, name):
                attr = getattr(self.data, name)
                if callable(attr):
                    self.data = attr(*args, **kwargs)
            return self
        return wrapper

    def execute(self) -> Any:
        return self.data

def batch_process(func: Callable) -> Callable:
    """Decorator for transforming individual items into collection-safe execution."""
    @functools.wraps(func)
    def wrapper(data: Any, *args, **kwargs) -> Any:
        if isinstance(data, (list, tuple, set)):
            return type(data)(func(item, *args, **kwargs) for item in data)
        return func(data, *args, **kwargs)
    return wrapper

def schema_enforcer(schema: Dict[str, type]) -> Callable:
    """Runtime validation of dictionary-like structures."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)
            if isinstance(result, dict):
                for key, expected_type in schema.items():
                    if not isinstance(result.get(key), expected_type):
                        raise TypeError(f"Key {key} expects {expected_type}")
            return result
        return wrapper
    return decorator