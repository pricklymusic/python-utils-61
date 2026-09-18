import time
import functools
import logging

logger = logging.getLogger(__name__)

def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)): 
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_ex = e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

class NetworkRetryError(Exception):
    """Custom exception for exhausted retry attempts."""
    pass

def execute_with_retry(func, *args, **kwargs):
    try:
        return retry(max_attempts=3)(func)(*args, **kwargs)
    except Exception as e:
        raise NetworkRetryError(f"Operation failed after retries: {e}") from e