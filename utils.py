import time
import functools
import random

def retry_network(max_attempts=3, backoff=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    sleep_time = backoff * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

@retry_network(max_attempts=4)
def fetch_data(url):
    # Simulate network instability
    if random.random() < 0.7:
        raise ConnectionError('network flap')
    return f'success from {url}'