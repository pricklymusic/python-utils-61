import time
import functools
import random

def retry_network_op(max_attempts=3, base_delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = (base_delay * (2 ** (attempts - 1))) + random.uniform(0, 1)
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

def validate_connection(func):
    @functools.wraps(func)
    def checker(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            raise ValueError('Operation yielded empty result')
        return result
    return checker