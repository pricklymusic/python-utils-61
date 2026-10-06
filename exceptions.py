import time
import functools
import logging

class TransientNetworkError(Exception):
    """Custom exception for retryable network issues."""

def retry_with_backoff(retries=3, delay=1, backoff=2):
    """A decorator for exponential backoff on network calls."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ntries, nwait = retries, delay
            while ntries > 1:
                try:
                    return func(*args, **kwargs)
                except (TransientNetworkError, ConnectionError) as e:
                    logging.warning(f"Retrying in {nwait}s due to: {e}")
                    time.sleep(nwait)
                    ntries -= 1
                    nwait *= backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator

class NetworkCircuitBreaker:
    """Context manager to limit repeated network failures."""
    def __init__(self, limit=5):
        self.limit = limit
        self.failures = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, (TransientNetworkError, ConnectionError)):
            self.failures += 1
            if self.failures >= self.limit:
                raise RuntimeError("Circuit breaker tripped")
        return False