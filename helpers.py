import time
import functools
import random

def resilient(retries=3, backoff=1.5, exceptions=(Exception,)): 
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = backoff
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    time.sleep(current_delay * (1 + random.random() * 0.1))
                    current_delay *= backoff
        return wrapper
    return decorator

def execute_with_jitter(task_func, *args, **kwargs):
    """execute arbitrary callable with adaptive retry logic"""
    wrapped = resilient()(task_func)
    return wrapped(*args, **kwargs)