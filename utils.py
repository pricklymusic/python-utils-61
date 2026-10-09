import functools
import itertools
import operator
from typing import Any, Callable, Iterable, List, TypeVar

T = TypeVar('T')

def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Chain a sequence of functions into a single pipeline."""
    return lambda x: functools.reduce(lambda v, f: f(v), functions, x)

def flatten(items: Iterable[Iterable[T]]) -> List[T]:
    """Collapse nested iterables into a flat list using itertools."""
    return list(itertools.chain.from_iterable(items))

def chunker(iterable: Iterable[T], n: int) -> Iterable[List[T]]:
    """Slice an iterable into chunks of fixed size n."""
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))

def memoize_by_attr(attr: str) -> Callable:
    """Cache function results based on an object attribute."""
    def decorator(func: Callable):
        cache = {}
        @functools.wraps(func)
        def wrapper(obj):
            key = getattr(obj, attr)
            if key not in cache:
                cache[key] = func(obj)
            return cache[key]
        return wrapper
    return decorator

def silent_map(func: Callable[[T], Any], items: Iterable[T]) -> List[Any]:
    """Execute function on items, suppressing and skipping errors."""
    results = []
    for item in items:
        try:
            results.append(func(item))
        except Exception:
            continue
    return results