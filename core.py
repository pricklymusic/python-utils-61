import functools
import itertools
import time
from typing import Callable, Any

def compose(*functions: Callable) -> Callable:
    return lambda x: functools.reduce(lambda v, f: f(v), functions, x)

def memoize_with_expiry(ttl: int = 60):
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < ttl:
                    return result
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

def chunker(iterable: Any, size: int):
    it = iter(iterable)
    return iter(lambda: tuple(itertools.islice(it, size)), ())

def flatten(nested: list) -> list:
    return [item for sublist in nested for item in sublist]

def retry(attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if i == attempts - 1: raise
                    time.sleep(delay)
        return wrapper
    return decorator