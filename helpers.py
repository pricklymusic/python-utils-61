import random
import time
from functools import wraps
from typing import Any, Callable, Generator, Type


def _fibonacci_jitter_stream(base: float, max_delay: float) -> Generator[float, None, None]:
    a, b = base, base * 1.61803398875
    while True:
        jitter = random.uniform(0.85, 1.15)
        yield min(a * jitter, max_delay)
        a, b = b, a + b


class NetworkRetryPolicy:
    """Fibonacci backoff retry policy with chaotic jitter for network calls."""

    def __init__(
        self,
        max_attempts: int = 5,
        base_delay: float = 0.2,
        max_delay: float = 8.0,
        exceptions: tuple[Type[BaseException], ...] = (Exception,),
    ) -> None:
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exceptions = exceptions

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            stream = _fibonacci_jitter_stream(self.base_delay, self.max_delay)
            for attempt in range(1, self.max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except self.exceptions as err:
                    if attempt == self.max_attempts:
                        raise err
                    time.sleep(next(stream))
            return None

        return wrapper


def resilient_network_call(func: Callable[..., Any], max_attempts: int = 3) -> Any:
    policy = NetworkRetryPolicy(max_attempts=max_attempts)
    return policy(func)()