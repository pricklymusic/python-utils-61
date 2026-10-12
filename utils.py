import time
import functools
from typing import Callable, Any, Type

def retry_on_failure(max_retries: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)): 
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= max_retries:
                        raise e
                    time.sleep(delay * (2 ** (attempts - 1)))
            return None
        return wrapper
    return decorator

class ExponentialBackoffHandler:
    def __init__(self, target_func: Callable, retries: int = 3):
        self.target = target_func
        self.limit = retries

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return retry_on_failure(max_retries=self.limit)(self.target)(*args, **kwargs)