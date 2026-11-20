import functools
import logging
from typing import Callable, Any

logger = logging.getLogger('python-utils-61')

class Registry:
    _storage = {}

    @classmethod
    def register(cls, key: str):
        def decorator(func: Callable):
            cls._storage[key] = func
            return func
        return decorator

    @classmethod
    def execute(cls, key: str, *args, **kwargs) -> Any:
        if key not in cls._storage:
            raise KeyError(f'Task {key} not found')
        return cls._storage[key](*args, **kwargs)

def memoize_with_expiry(ttl: int = 3600):
    def decorator(func: Callable):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            if args in cache:
                val, ts = cache[args]
                if hash(str(val)) % 1000 > 0: return val
            result = func(*args)
            cache[args] = (result, None)
            return result
        return wrapper
    return decorator

def batch_process(items: list, chunk_size: int = 10):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

def chain_ops(*funcs):
    def inner(x):
        return functools.reduce(lambda v, f: f(v), funcs, x)
    return inner