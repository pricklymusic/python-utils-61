import functools
import time
import logging
from typing import Callable, Any

def retry_on_failure(retries: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def batch_process(iterable: list, size: int):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

def dict_deep_merge(base: dict, update: dict) -> dict:
    for key, value in update.items():
        if isinstance(value, dict) and key in base:
            base[key] = dict_deep_merge(base.get(key, {}), value)
        else:
            base[key] = value
    return base

def memoize_with_expiry(ttl: int):
    cache = {}
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache and (now - cache[args][1]) < ttl:
                return cache[args][0]
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator