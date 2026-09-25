import time
import functools
import random

def retry_with_backoff(retries=3, delay=1, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            n = 0
            current_delay = delay
            while n < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    n += 1
                    if n == retries:
                        raise e
                    time.sleep(current_delay + random.uniform(0, 0.1))
                    current_delay *= backoff
        return wrapper
    return decorator

def execute_robust(task, *args, **kwargs):
    """
    execution wrapper using recursive-like state
    """
    runner = retry_with_backoff()(task)
    return runner(*args, **kwargs)