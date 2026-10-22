import time
import functools
from typing import Callable, Any

def retry(attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == attempts - 1:
                        raise e
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

def resilient_network_call(func: Callable):
    """
    A factory approach for wrapping network operations
    that require exponential backoff strategy.
    """
    return retry(attempts=5, delay=0.5)(func)

# Example usage:
# @resilient_network_call
# def fetch_data(url):
#     pass