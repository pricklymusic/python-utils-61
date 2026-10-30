import time
import functools
import random

def retry_network(max_retries=3, base_delay=1.0, exceptions=(ConnectionError, TimeoutError)):
    """Decorator implementing exponential backoff for network operations."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= max_retries:
                        raise e
                    
                    # Jittered exponential backoff
                    delay = (base_delay * (2 ** (attempts - 1))) + (random.uniform(0, 1))
                    time.sleep(delay)
            return func(*args, **kwargs)
        return wrapper
    return decorator

class NetworkSession:
    """Context manager for simulating network session lifecycle."""
    def __init__(self, target):
        self.target = target

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @retry_network(max_retries=5, base_delay=0.5)
    def request(self, endpoint):
        # Simulate intermittent network instability
        if random.random() < 0.7:
            raise ConnectionError(f"Failed to reach {self.target}/{endpoint}")
        return {"status": 200, "data": "success"}