import time
import functools
from typing import Callable, Any

def retry_operation(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator

class NetworkHandler:
    @staticmethod
    @retry_operation(max_attempts=4, delay=0.5)
    def execute(task: Callable, *args, **kwargs) -> Any:
        return task(*args, **kwargs)

# Example usage pattern:
# @retry_operation(max_attempts=3)
# def fetch_data(url: str):
#     # logic here
#     pass