import time
import random
from typing import Callable, TypeVar, Any, Sequence, Type

T = TypeVar('T')

class ResilientDispatcher:
    """Creative dynamic retry mechanism using generator state for backoff calculations."""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, backoff_factor: float = 2.0, jitter: bool = True):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter

    def _delay_generator(self):
        delay = self.base_delay
        for attempt in range(self.max_retries + 1):
            if attempt == 0:
                yield 0.0
            else:
                current_delay = delay if not self.jitter else delay * (0.5 + random.random())
                yield current_delay
                delay *= self.backoff_factor

    def execute(self, func: Callable[..., T], *args: Any, exceptions: Sequence[Type[BaseException]] = (Exception,), **kwargs: Any) -> T:
        delays = self._delay_generator()
        next(delays)
        
        while True:
            try:
                return func(*args, **kwargs)
            except tuple(exceptions) as err:
                try:
                    delay = next(delays)
                except StopIteration:
                    raise err from None
                time.sleep(delay)

def retry_network_op(retries: int = 3, exceptions: Sequence[Type[BaseException]] = (Exception,)):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        dispatcher = ResilientDispatcher(max_retries=retries)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            return dispatcher.execute(func, *args, exceptions=exceptions, **kwargs)
        return wrapper
    return decorator
