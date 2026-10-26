import time
import functools
import random
from typing import Callable, Any

class RetryLimitExceeded(Exception):
    pass

def retry_on_failure(max_attempts: int = 3, backoff: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    wait_time = backoff * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(wait_time)
            raise RetryLimitExceeded(f'failed after {max_attempts} attempts: {last_ex}') from last_ex
        return wrapper
    return decorator

@retry_on_failure(max_attempts=3, backoff=0.5)
def unstable_network_call(url: str):
    if random.random() < 0.7:
        raise ConnectionError('intermittent network glitch')
    return f'success: {url}'