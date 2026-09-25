import time
import functools
import random
from typing import Callable, Any

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempts, current_delay = 0, delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    time.sleep(current_delay + random.uniform(0, 0.1))
                    current_delay *= backoff
        return wrapper
    return decorator

def execute_with_fallback(operation: Callable, fallback_value: Any = None):
    try:
        return operation()
    except Exception:
        return fallback_value

class NetworkSession:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    @retry(max_attempts=3, delay=0.5)
    def fetch_data(self, url: str):
        print(f"Accessing {url}...")
        if random.random() < 0.7:
            raise ConnectionError("Transient network instability")
        return {"status": 200, "data": "success"}