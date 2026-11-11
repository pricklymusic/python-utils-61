import functools
import itertools
import time
from typing import Any, Callable, Iterable, TypeVar

T = TypeVar('T')

def retry_on_failure(retries: int = 3, delay: float = 0.5) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if i == retries - 1:
                        raise
                    time.sleep(delay * (2 ** i))
        return wrapper
    return decorator

def chunk_iterator(data: Iterable[T], size: int) -> Iterable[list[T]]:
    it = iter(data)
    while True:
        chunk = list(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk

def compose(*functions: Callable) -> Callable:
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions)

def pluck(items: Iterable[dict], key: str, default: Any = None) -> list[Any]:
    return [item.get(key, default) for item in items]

def smart_flatten(items: Iterable) -> list:
    flat = []
    for item in items:
        if isinstance(item, (list, tuple, set)):
            flat.extend(smart_flatten(item))
        else:
            flat.append(item)
    return flat