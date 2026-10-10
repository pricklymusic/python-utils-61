import time
import functools
import random
from typing import Callable, Any

def retry_operation(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        sleep_time = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                        time.sleep(sleep_time)
            raise last_exception
        return wrapper
    return decorator

class NetworkProcessor:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    @retry_operation(max_attempts=4, base_delay=0.5)
    def fetch_data(self, url: str) -> str:
        # Simulated network unpredictability
        if random.random() < 0.7:
            raise ConnectionError(f"Failed to reach {url}")
        return f"data_from_{url}"