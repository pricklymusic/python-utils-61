import functools
import time
import itertools
from typing import Any, Callable, Iterable, TypeVar

T = TypeVar('T')

def batch_process(iterable: Iterable[T], n: int) -> Iterable[tuple[T, ...]]:
    args = [iter(iterable)] * n
    return zip(*args, strict=False)

def retry_execution(retries: int = 3, delay: float = 0.5):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_err = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_err = e
                    time.sleep(delay * (2 ** i))
            raise last_err
        return wrapper
    return decorator

def deep_getattr(obj: Any, path: str, default: Any = None) -> Any:
    try:
        return functools.reduce(getattr, path.split('.'), obj)
    except AttributeError:
        return default

def memoize_with_expiry(ttl: float = 60):
    cache = {}
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in cache and (now - cache[key]['ts'] < ttl):
                return cache[key]['val']
            result = func(*args, **kwargs)
            cache[key] = {'val': result, 'ts': now}
            return result
        return wrapper
    return decorator