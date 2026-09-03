import time
import random
import functools
from typing import Callable, Any, Tuple, Type

def backoff_generator(base_delay: float = 1.0, max_delay: float = 60.0, factor: float = 2.0):
    delay = base_delay
    while True:
        yield random.uniform(0, min(max_delay, delay))
        delay *= factor

def retry_network_op(
    max_retries: int = 3,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    base_delay: float = 0.5
):
    """Decorator applying exponential jitter backoff to network functions."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delays = backoff_generator(base_delay=base_delay)
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    if attempt == max_retries:
                        raise err
                    time.sleep(next(delays))
        return wrapper
    return decorator
