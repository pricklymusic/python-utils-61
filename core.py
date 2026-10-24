import time
import random
import functools
from typing import Callable, Any, Type, Sequence, Generator, Optional


def fibonacci_jitter_backoff(base: float = 0.5, cap: float = 30.0) -> Generator[float, None, None]:
    a, b = base, base
    while True:
        jittered = a + random.uniform(0, a * 0.3)
        yield min(jittered, cap)
        a, b = b, a + b


class RetryExhaustedError(Exception):
    """Raised when all retry attempts fail."""
    def __init__(self, last_exception: BaseException, attempts: int):
        super().__init__(f"Exhausted {attempts} attempts. Last exception: {last_exception}")
        self.last_exception = last_exception
        self.attempts = attempts


def retry_network(
    exceptions: Sequence[Type[BaseException]] = (Exception,),
    max_attempts: int = 4,
    backoff_factory: Callable[[], Generator[float, None, None]] = fibonacci_jitter_backoff,
    on_retry: Optional[Callable[[BaseException, int, float], None]] = None,
):
    """Decorator executing network operations with configurable backoff strategies."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delays = backoff_factory()
            last_err: Optional[BaseException] = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions) as err:
                    last_err = err
                    if attempt == max_attempts:
                        break
                    
                    delay = next(delays)
                    if on_retry:
                        on_retry(err, attempt, delay)
                    time.sleep(delay)
            
            raise RetryExhaustedError(last_err, max_attempts) from last_err
        
        return wrapper
    return decorator
