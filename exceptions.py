import time
import functools
from typing import Callable, Any, Type, Tuple

def retry(exceptions: Tuple[Type[Exception], ...] = (Exception,), retries: int = 3, delay: float = 1.0) -> Callable:
    """Decorator applying exponential backoff for network operations"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            current_delay = delay
            for i in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_ex = e
                    if i < retries:
                        time.sleep(current_delay)
                        current_delay *= 2
                    else:
                        break
            raise last_ex
        return wrapper
    return decorator

class NetworkError(Exception):
    """Base exception for network operations"""
    pass

class TimeoutError(NetworkError):
    """Specific timeout condition"""
    pass

class ConnectionRefusedError(NetworkError):
    """Server rejected connection"""
    pass