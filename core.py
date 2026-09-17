import collections
import functools
from typing import Any, Callable, TypeVar

T = TypeVar('T')

class Registry:
    def __init__(self):
        self._storage = collections.defaultdict(list)

    def register(self, tag: str):
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            self._storage[tag].append(func)
            return func
        return decorator

    def execute(self, tag: str, *args: Any, **kwargs: Any) -> list[Any]:
        return [f(*args, **kwargs) for f in self._storage.get(tag, [])]

class Singleton(type):
    _instances: dict[Any, Any] = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

def memoize_with_expiry(ttl: int):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            import time
            now = time.time()
            if args in cache:
                val, ts = cache[args]
                if now - ts < ttl:
                    return val
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator

app_registry = Registry()