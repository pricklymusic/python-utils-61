import time
import functools
from typing import Callable, Any

def retry_operation(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        sleep_time = delay * (2 ** attempt)
                        time.sleep(sleep_time)
                    continue
            raise last_exception
        return wrapper
    return decorator

class NetworkHandler:
    @staticmethod
    @retry_operation(max_attempts=3, delay=0.5)
    def execute(request_func: Callable, *args, **kwargs) -> Any:
        return request_func(*args, **kwargs)