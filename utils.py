import time
import functools
from typing import Callable, Any, Type

def retry_on_failure(exceptions: tuple[Type[Exception], ...], max_retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_ex = e
                    if attempt < max_retries:
                        time.sleep(delay * (2 ** attempt))
                    else:
                        raise last_ex
            return None
        return wrapper
    return decorator

class NetworkCircuit:
    """Context manager for suppressing noise during retries."""
    def __init__(self, silent: bool = True):
        self.silent = silent

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.silent and exc_type:
            return True
        return False