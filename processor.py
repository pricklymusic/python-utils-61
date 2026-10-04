import time
import functools
import random
from typing import Callable, Any, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def retry_network_call(max_attempts: int = 3, base_delay: float = 1.0) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = base_delay * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@retry_network_call(max_attempts=4, base_delay=0.5)
def fetch_remote_resource(url: str) -> str:
    # simulate network unpredictability
    if random.random() < 0.7:
        raise ConnectionError("Network flicker encountered")
    return f"Payload from {url}"