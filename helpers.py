import functools
import logging
from typing import Callable, Any, Dict

logger = logging.getLogger(__name__)

class Registry:
    _storage: Dict[str, Any] = {}

    @classmethod
    def register(cls, key: str):
        def decorator(func: Callable):
            cls._storage[key] = func
            return func
        return decorator

    @classmethod
    def execute(cls, key: str, *args, **kwargs):
        if key not in cls._storage:
            raise ValueError(f'key {key} not found')
        return cls._storage[key](*args, **kwargs)

def memoize_with_expiry(ttl: int = 300):
    def decorator(func: Callable):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key in cache:
                return cache[key]
            result = func(*args, **kwargs)
            cache[key] = result
            return result
        return wrapper
    return decorator

def batch_process(items: list, chunk_size: int = 10):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

def sanitize_input(data: str) -> str:
    return ''.join(char for char in data if char.isalnum() or char.isspace()).strip()