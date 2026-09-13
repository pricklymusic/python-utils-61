import functools
import time
import operator
from typing import Any, Callable, Iterable

def compose(*functions: Callable) -> Callable:
    return lambda x: functools.reduce(lambda v, f: f(v), functions, x)

def memoize(func: Callable) -> Callable:
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

def throttle(seconds: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        last_called = 0
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_called
            elapsed = time.time() - last_called
            if elapsed < seconds:
                return None
            last_called = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def flatten(nested: Iterable) -> list:
    flat = []
    for item in nested:
        if isinstance(item, (list, tuple)):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat

def pipeline(data: Any, *funcs: Callable) -> Any:
    return compose(*funcs)(data)

def chunker(seq: Iterable, size: int) -> Iterable:
    for i in range(0, len(seq), size):
        yield seq[i:i + size]