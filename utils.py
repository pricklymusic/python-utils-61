import functools
import itertools
import time
from typing import Any, Callable, Iterable, TypeVar

T = TypeVar('T')

def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions)

def chunks(iterable: Iterable[T], size: int) -> Iterable[list[T]]:
    iterator = iter(iterable)
    for first in iterator:
        yield [first] + list(itertools.islice(iterator, size - 1))

def throttled(interval: float) -> Callable[[Callable], Callable]:
    def decorator(func: Callable) -> Callable:
        last_called = [0.0]
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            elapsed = time.time() - last_called[0]
            if elapsed < interval:
                time.sleep(interval - elapsed)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def deep_get(obj: dict, path: str, default: Any = None) -> Any:
    try:
        return functools.reduce(lambda d, key: d[key], path.split('.'), obj)
    except (KeyError, TypeError):
        return default

def memoize_instance(func: Callable) -> Callable:
    cache = {}
    @functools.wraps(func)
    def wrapper(self, *args: Any) -> Any:
        key = (id(self), args)
        if key not in cache:
            cache[key] = func(self, *args)
        return cache[key]
    return wrapper