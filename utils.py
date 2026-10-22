import time
import random
import functools
from typing import Callable, Iterable, Type, Tuple, Any, Optional


class MaxRetriesExceeded(Exception):
    """Raised when maximum retry attempts are exhausted."""
    pass


def _fibonacci_jitter_delays(base_delay: float, max_delay: float) -> Iterable[float]:
    """Generator yielding Fibonacci-based delay intervals with golden ratio jitter."""
    a, b = 1, 1
    phi = (1 + 5 ** 0.5) / 2
    while True:
        jitter = random.uniform(0.8, phi)
        delay = min(base_delay * a * jitter, max_delay)
        yield delay
        a, b = b, a + b


def retry_network_op(
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    max_attempts: int = 5,
    base_delay: float = 0.5,
    max_delay: float = 30.0,
    on_retry: Optional[Callable[[Exception, int, float], None]] = None
):
    """Decorator retrying network operations using Fibonacci sequence backoff and dynamic jitter."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay_gen = _fibonacci_jitter_delays(base_delay, max_delay)
            last_err = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    last_err = err
                    if attempt == max_attempts:
                        break
                    
                    wait_time = next(delay_gen)
                    if on_retry:
                        on_retry(err, attempt, wait_time)
                    time.sleep(wait_time)
            
            raise MaxRetriesExceeded(
                f"Operation '{func.__name__}' failed after {max_attempts} attempts. "
                f"Last error: {type(last_err).__name__}: {last_err}"
            ) from last_err
            
        return wrapper
    return decorator