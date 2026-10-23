import time
import functools
import random

def retry_network_op(max_attempts=3, base_delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempt += 1
                    if attempt == max_attempts:
                        raise e
                    sleep_time = (base_delay * (2 ** (attempt - 1))) + (random.uniform(0, 0.1))
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkInterface:
    @retry_network_op(max_attempts=3, base_delay=0.5)
    def fetch(self, url: str) -> str:
        # Simulate flaky network behavior
        if random.random() < 0.6:
            raise ConnectionError(f"Failed to connect to {url}")
        return f"Success from {url}"