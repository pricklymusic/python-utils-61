import time
import functools
from typing import Callable, Any, Type

def retry_on_failure(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)): 
    """Decorator applying exponential backoff for transient failures."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            current_delay = delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(current_delay)
                        current_delay *= 2
            raise last_exception
        return wrapper
    return decorator

class NetworkProcessor:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    @retry_on_failure(max_attempts=4, delay=0.5)
    def fetch_data(self, key: str) -> str:
        # Simulated unstable network call
        import random
        if random.random() < 0.7:
            raise ConnectionError(f"Failed to connect to {self.endpoint}")
        return f"data_for_{key}"