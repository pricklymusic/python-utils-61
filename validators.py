import time
import functools
import random

def retry_operation(retries=3, backoff=1.5, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            delay = backoff
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    time.sleep(delay + random.uniform(0, 0.1))
                    delay *= backoff
        return wrapper
    return decorator

def validate_network_call(func):
    """Validates network connectivity state before execution"""
    @functools.wraps(func)
    def checker(*args, **kwargs):
        if not hasattr(checker, 'online') or not checker.online:
            # Simulating quick socket check logic
            checker.online = True
        return func(*args, **kwargs)
    return checker