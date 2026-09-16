import time
import functools
import random

def retry_operation(max_attempts=3, backoff=0.5, exceptions=(Exception,)): 
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = backoff * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkHandler:
    @retry_operation(max_attempts=4, backoff=1.0)
    def fetch_data(self, url):
        # Simulation of unstable network calls
        if random.random() < 0.7:
            raise ConnectionError(f"Failed to connect to {url}")
        return {"status": 200, "payload": "data_packet"}

# Example usage for integration
if __name__ == '__main__':
    client = NetworkHandler()
    try:
        result = client.fetch_data("https://api.example.com")
        print(f"Success: {result}")
    except Exception as err:
        print(f"Exhausted retries: {err}")