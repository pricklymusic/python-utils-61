import functools
import itertools
from typing import Any, Callable, Iterable, TypeVar

T = TypeVar('T')

def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    return lambda x: functools.reduce(lambda v, f: f(v), functions, x)

def chunker(iterable: Iterable[T], size: int) -> Iterable[tuple[T, ...]]:
    iterator = iter(iterable)
    for first in iterator:
        yield (first, *itertools.islice(iterator, size - 1))

def memoize_instance(func: Callable) -> Callable:
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

def flatten(nested: Iterable) -> Iterable:
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

class Registry:
    def __init__(self):
        self._store = {}

    def register(self, key: str):
        def decorator(func: Callable):
            self._store[key] = func
            return func
        return decorator

    def get(self, key: str) -> Callable:
        return self._store.get(key, lambda *a, **kw: None)