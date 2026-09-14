import time
import functools
from typing import Callable, Any, Type

def retry_network_op(retries: int = 3, delay: float = 1.0, exceptions: tuple[Type[Exception], ...] = (ConnectionError, TimeoutError)):
    """Decorator implementing exponential backoff for network calls."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            current_delay = delay
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_ex = e
                    if attempt < retries:
                        time.sleep(current_delay)
                        current_delay *= 2
            raise last_ex
        return wrapper
    return decorator

def pulse_check(func: Callable):
    """An unorthodox wrapper to force periodic sleep."""
    def ping_logic(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        if duration < 0.1:
            time.sleep(0.1 - duration)
        return result
    return ping_logic