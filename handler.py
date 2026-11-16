import functools
import time
import threading
from typing import Callable, Any

def retry_with_backoff(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

class ConcurrentStore:
    def __init__(self):
        self._data = {}
        self._lock = threading.Lock()

    def atomic_update(self, key: str, op: Callable[[Any], Any]):
        with self._lock:
            self._data[key] = op(self._data.get(key))
        return self._data[key]

def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def memoize_by_attr(attr: str):
    def decorator(func: Callable):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = getattr(args[0], attr)
            if key not in cache:
                cache[key] = func(*args, **kwargs)
            return cache[key]
        return wrapper
    return decorator