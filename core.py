import functools
import itertools
import time
from typing import Any, Callable, Iterable, TypeVar

T = TypeVar('T')

def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions)

def flatten(nested: Iterable[Any]) -> Iterable[Any]:
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

def throttle(seconds: float) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        last_called = [0.0]
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            elapsed = time.time() - last_called[0]
            if elapsed < seconds:
                time.sleep(seconds - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

def batch(iterable: Iterable[T], n: int) -> Iterable[tuple[T, ...]]:
    args = [iter(iterable)] * n
    return zip(*args, strict=False)

def memoize_with_expiry(ttl: int) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache: dict[tuple[Any, ...], tuple[float, T]] = {}
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in cache and now - cache[key][0] < ttl:
                return cache[key][1]
            result = func(*args, **kwargs)
            cache[key] = (now, result)
            return result
        return wrapper
    return decorator