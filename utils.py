import time
import functools
import random

def retry(max_attempts=3, delay=1, backoff=2):
    """Decorator implementing exponential backoff for network operations."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    time.sleep(current_delay + random.uniform(0, 0.1))
                    current_delay *= backoff
        return wrapper
    return decorator

def with_context(operation_name):
    """Helper for wrapping network calls with logging context."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                print(f"Executing operation: {operation_name}")
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Operation {operation_name} failed: {e}")
                raise
        return wrapper
    return decorator