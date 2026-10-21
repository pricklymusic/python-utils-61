import time
import functools
import random

def retry_operation(max_attempts=3, base_delay=1.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    sleep_time = base_delay * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

@retry_operation(max_attempts=3, base_delay=0.5)
def fetch_data(url):
    # Simulate volatile network operation
    if random.random() < 0.7:
        raise ConnectionError("Network flicker detected")
    return f"Payload from {url}"