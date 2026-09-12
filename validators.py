import time
import random
from typing import Callable, Any, Tuple, Type

def fibonacci_backoff(base: float = 1.0):
    a, b = base, base
    while True:
        yield a + random.uniform(0, 0.2 * a)
        a, b = b, a + b

def retry_with_validation(
    retries: int = 3,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    validator: Callable[[Any], bool] = lambda x: True
):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            backoff = fibonacci_backoff()
            for attempt in range(retries + 1):
                try:
                    result = func(*args, **kwargs)
                    if validator(result):
                        return result
                    raise ValueError("Validation failed for network response")
                except exceptions as err:
                    if attempt == retries:
                        raise err
                    delay = next(backoff)
                    time.sleep(delay)
            raise RuntimeError("Retry limit reached")
        return wrapper
    return decorator