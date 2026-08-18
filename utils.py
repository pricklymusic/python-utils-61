import time
import random

class NetworkError(Exception):
    pass

def network_operation():
    if random.choice([True, False]):
        raise NetworkError("Simulated network failure")
    return "Network operation successful"

def retry_decorator(retries=3, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except NetworkError as e:
                    attempt += 1
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        time.sleep(delay)
            raise NetworkError(f"All {retries} attempts failed")
        return wrapper
    return decorator

@retry_decorator(retries=5, delay=1)
def perform_network_task():
    result = network_operation()
    print(result)
    return result

if __name__ == '__main__':
    perform_network_task()