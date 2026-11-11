import collections
import functools
from typing import Any, Callable, Iterable, TypeVar

T = TypeVar('T')

class DataPipeline:
    def __init__(self, data: Iterable[T]):
        self._data = list(data)

    def pipe(self, func: Callable[[Iterable[T]], Iterable[T]]) -> 'DataPipeline':
        self._data = list(func(self._data))
        return self

    def collect(self) -> list[T]:
        return self._data

def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def composition(x: Any) -> Any:
        return functools.reduce(lambda acc, f: f(acc), functions, x)
    return composition

def flatten(items: Iterable[Any]) -> list[Any]:
    result = []
    for item in items:
        if isinstance(item, collections.abc.Iterable) and not isinstance(item, (str, bytes)):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

def memoize_instance(func: Callable) -> Callable:
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper