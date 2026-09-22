import time
import functools
import random
from typing import Callable, Any

def retry_with_backoff(retries: int = 3, base_delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    sleep_time = (base_delay * (2 ** attempt)) + (random.uniform(0, 0.1))
                    time.sleep(sleep_time)
            raise last_exception
        return wrapper
    return decorator

class NetworkCircuit:
    def __init__(self, target_func: Callable):
        self.target = target_func
    
    def execute(self, *args, **kwargs) -> Any:
        proxy = retry_with_backoff()(self.target)
        return proxy(*args, **kwargs)