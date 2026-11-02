import collections
import functools
from typing import Any, Callable, Dict, List

class Registry:
    def __init__(self):
        self._storage: Dict[str, Any] = {}

    def __setitem__(self, key: str, value: Any) -> None:
        self._storage[key] = value

    def __getitem__(self, key: str) -> Any:
        return self._storage.get(key)

    def clear_nones(self) -> None:
        self._storage = {k: v for k, v in self._storage.items() if v is not None}

def memoize_with_ttl(ttl_seconds: int):
    def decorator(func: Callable):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            import time
            now = time.time()
            if args in cache and (now - cache[args][1]) < ttl_seconds:
                return cache[args][0]
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator

def flatten_deep(items: List) -> List:
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from flatten_deep(item)
        else:
            yield item

class ContextPipe:
    def __init__(self, data: Any):
        self.data = data

    def pipe(self, *funcs: Callable) -> Any:
        return functools.reduce(lambda acc, f: f(acc), funcs, self.data)

GLOBAL_REGISTRY = Registry()