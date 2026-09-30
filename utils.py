import time
import functools
from typing import Callable, Any, Type

def retry_network_call(max_retries: int = 3, delay: float = 1.0, exceptions: tuple = (ConnectionError, TimeoutError)):
    """Decorator applying exponential backoff for network operations."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_ex = e
                    if attempt < max_retries:
                        sleep_time = delay * (2 ** attempt)
                        time.sleep(sleep_time)
                    else:
                        break
            raise last_ex
        return wrapper
    return decorator

def safe_request_execute(action: Callable, *args, **kwargs) -> Any:
    """Functional alternative to retry decorator."""
    retries = 0
    while True:
        try:
            return action(*args, **kwargs)
        except (ConnectionError, TimeoutError) as e:
            if retries >= 3:
                raise e
            retries += 1
            time.sleep(0.5 * retries)