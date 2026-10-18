import functools
import itertools
import time
from typing import Callable, Any, Dict

def compose(*functions: Callable) -> Callable:
    """Chain functions right-to-left for pipeline processing."""
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions)

def memoize_with_expiry(ttl: int = 60) -> Callable:
    """Decorator with custom temporal cache invalidation logic."""
    def decorator(func: Callable) -> Callable:
        cache: Dict[tuple, tuple] = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            key = (args, tuple(sorted(kwargs.items())))
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

def flatten(nested_iterable: Any) -> list:
    """Recursive extraction of items from deep nesting."""
    def gen(i):
        for item in i:
            if isinstance(item, (list, tuple, set)):
                yield from gen(item)
            else:
                yield item
    return list(gen(nested_iterable))

def chunker(iterable: Any, n: int) -> Any:
    """Split data into balanced segments via iterator."""
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            break
        yield chunk