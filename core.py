import time
import functools
import random

def retry_network(max_attempts=3, backoff=0.5):
    """Decorator implementing exponential backoff with jitter."""
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
                    sleep_time = (backoff * (2 ** attempts)) + (random.random() * 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkProxy:
    def __init__(self, target_url):
        self.target = target_url

    @retry_network(max_attempts=4, backoff=1.0)
    def fetch_data(self, endpoint):
        # Simulate unstable network condition
        if random.random() < 0.7:
            raise ConnectionError(f"Failed to reach {self.target}/{endpoint}")
        return {"status": 200, "payload": "data_packet"}

if __name__ == "__main__":
    client = NetworkProxy("https://api.example.com")
    result = client.fetch_data("v1/resource")
    print(result)