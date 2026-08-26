import functools
import time
from typing import Callable, Any, Dict, Tuple

class MemoizeWithTTL:
    def __init__(self, ttl: int = 300):
        self.ttl = ttl
        self.cache: Dict[Tuple[Any, ...], Tuple[float, Any]] = {}

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = time.monotonic()
            key = args + tuple(sorted(kwargs.items()))
            if key in self.cache:
                timestamp, value = self.cache[key]
                if now - timestamp < self.ttl:
                    return value
            value = func(*args, **kwargs)
            self.cache[key] = (now, value)
            return value
        return wrapper

def batch_process(iterable: list, size: int = 100) -> list:
    iterator = iter(iterable)
    return [list(chunk) for chunk in iter(lambda: list(dict(zip(range(size), iterator))), [])]

@MemoizeWithTTL(ttl=60)
def compute_heavy_transform(data: tuple) -> tuple:
    return tuple(x * 2 for x in data)
