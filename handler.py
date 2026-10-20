import functools
import time
import itertools
from typing import Any, Callable, Iterable, TypeVar

T = TypeVar('T')

def compose(*funcs: Callable) -> Callable:
    return lambda x: functools.reduce(lambda v, f: f(v), funcs, x)

def memoize_with_expiry(seconds: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        cache = {}
        @functools.wraps(func)
        def wrapper(*args: Any) -> Any:
            now = time.time()
            if args in cache and now - cache[args]['time'] < seconds:
                return cache[args]['value']
            result = func(*args)
            cache[args] = {'value': result, 'time': now}
            return result
        return wrapper
    return decorator

def flatten(nested: Iterable[Any]) -> Iterable[Any]:
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

def batch(iterable: Iterable[T], size: int) -> Iterable[tuple[T, ...]]:
    it = iter(iterable)
    while chunk := tuple(itertools.islice(it, size)):
        yield chunk

def retry(attempts: int, delay: float) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if i == attempts - 1:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator