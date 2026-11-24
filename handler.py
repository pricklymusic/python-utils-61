import functools
import time
import collections
from typing import Callable, Any

def memoize_with_ttl(seconds: int = 3600):
    def decorator(func: Callable):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < seconds:
                    return result
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

def deep_flatten(items: list) -> list:
    flat = []
    for item in items:
        if isinstance(item, collections.abc.Iterable) and not isinstance(item, (str, bytes)):
            flat.extend(deep_flatten(item))
        else:
            flat.append(item)
    return flat

def compose(*functions: Callable) -> Callable:
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

class DataPipe:
    def __init__(self, data: Any):
        self.data = data

    def __or__(self, func: Callable):
        return DataPipe(func(self.data))

    def __repr__(self):
        return str(self.data)