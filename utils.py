import time
import functools
import random

def retry_operation(retries=3, backoff_factor=0.5, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    sleep_time = backoff_factor * (2 ** (attempt - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkHandler:
    @staticmethod
    @retry_operation(retries=3, backoff_factor=1.0)
    def execute_request(request_func, *args, **kwargs):
        return request_func(*args, **kwargs)