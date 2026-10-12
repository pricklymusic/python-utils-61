import time
import random
from typing import Type, Tuple, Optional, Any


class RetryAttempt:
    """Context manager representing a single attempt in a retry loop."""

    def __init__(self, loop: "RetryLoop") -> None:
        self.loop = loop

    def __enter__(self) -> "RetryAttempt":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Any,
    ) -> bool:
        if exc_type is None:
            self.loop.succeeded = True
            return True
        if issubclass(exc_type, self.loop.exceptions):
            self.loop.last_exception = exc_val
            return True
        return False


class RetryLoop:
    """Iterator for resilient execution of network operations using jittered backoff."""

    def __init__(
        self,
        max_attempts: int = 3,
        delay_base: float = 0.5,
        max_delay: float = 10.0,
        exceptions: Tuple[Type[Exception], ...] = (Exception,),
    ) -> None:
        self.max_attempts = max_attempts
        self.delay_base = delay_base
        self.max_delay = max_delay
        self.exceptions = exceptions
        self.succeeded = False
        self.last_exception: Optional[BaseException] = None
        self.current_attempt = 0

    def __iter__(self) -> "RetryLoop":
        return self

    def __next__(self) -> RetryAttempt:
        if self.succeeded:
            raise StopIteration
        if self.current_attempt >= self.max_attempts:
            if self.last_exception:
                raise RuntimeError(
                    f"Network operation failed after {self.max_attempts} attempts"
                ) from self.last_exception
            raise StopIteration

        if self.current_attempt > 0:
            calculated_delay = min(
                self.max_delay, self.delay_base * (2 ** (self.current_attempt - 1))
            )
            jittered_delay = random.uniform(0, calculated_delay)
            time.sleep(jittered_delay)

        self.current_attempt += 1
        return RetryAttempt(self)
