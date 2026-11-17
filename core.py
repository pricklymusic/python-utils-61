import functools
import itertools
import operator
from typing import Any, Callable, Iterable, TypeVar

T = TypeVar('T')

def compose(*funcs: Callable) -> Callable:
    """Right-to-left function composition using reduce."""
    return lambda x: functools.reduce(lambda v, f: f(v), reversed(funcs), x)

def chunker(iterable: Iterable[T], n: int) -> Iterable[tuple[T, ...]]:
    """Slicing iterables into fixed-size chunks."""
    it = iter(iterable)
    return iter(lambda: tuple(itertools.islice(it, n)), ())

def deep_get(obj: dict, path: str, default: Any = None) -> Any:
    """Dot-notation key access for nested structures."""
    try:
        return functools.reduce(operator.getitem, path.split('.'), obj)
    except (KeyError, TypeError, AttributeError):
        return default

def flip(func: Callable) -> Callable:
    """Argument order reversal for binary functions."""
    @functools.wraps(func)
    def wrapper(a, b):
        return func(b, a)
    return wrapper

def identity(x: T) -> T:
    """Pass-through utility for pipeline placeholders."""
    return x

def memoize_timed(ttl: int) -> Callable:
    """Simple TTL-based cache decorator logic."""
    def decorator(func: Callable) -> Callable:
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            import time
            now = time.time()
            if args in cache and (now - cache[args][1]) < ttl:
                return cache[args][0]
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator