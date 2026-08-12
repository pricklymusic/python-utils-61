import logging
import time
from functools import wraps

def retry(max_retries=3, wait_time=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logging.warning(f'Attempt {attempts} failed: {e}')
                    time.sleep(wait_time)
                    if attempts >= max_retries:
                        logging.error('Max retries exceeded')
                        raise
        return wrapper
    return decorator

@retry(max_retries=5, wait_time=1)
def network_request():
    # Simulate a network operation that may fail
    import random
    if random.choice([True, False]):
        raise ConnectionError('Network failure')
    return 'Success'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        result = network_request()
        logging.info(f'Network request result: {result}')
    except ConnectionError:
        logging.error('Network request ultimately failed')
