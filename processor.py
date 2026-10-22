import functools
import itertools
from typing import Callable, Any, Iterable

def chain_execute(data: Any, *functions: Callable) -> Any:
    """Sequentially pipe data through a sequence of callables."""
    return functools.reduce(lambda acc, f: f(acc), functions, data)

def partition_stream(predicate: Callable, stream: Iterable) -> tuple:
    """Split an iterable into two based on predicate truthiness."""
    true_list, false_list = [], []
    for item in stream:
        (true_list if predicate(item) else false_list).append(item)
    return true_list, false_list

def batch_process(iterable: Iterable, size: int) -> Iterable:
    """Slice an iterable into chunks of fixed size."""
    it = iter(iterable)
    return iter(lambda: list(itertools.islice(it, size)), [])

def memoize_method(func: Callable) -> Callable:
    """Method-level caching using attribute-bound storage."""
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

def safe_get(data: dict, keys: str, default: Any = None) -> Any:
    """Deep navigation of nested dictionary structures."""
    return functools.reduce(lambda d, k: d.get(k, {}) if isinstance(d, dict) else default, keys.split('.'), data) or default