import functools
import logging
import sys

logger = logging.getLogger(__name__)

def resilient_executor(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        retries = 3
        while retries > 0:
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, ZeroDivisionError) as e:
                logger.warning(f"Caught {type(e).__name__}: {e}. Retrying...")
                retries -= 1
                if retries == 0:
                    return None
            except Exception as e:
                logger.critical(f"Unrecoverable error: {e}")
                sys.exit(1)
    return wrapper

class EdgeCaseProcessor:
    def __init__(self, data=None):
        self.data = data or {}

    @resilient_executor
    def calculate_ratio(self, numerator, denominator):
        return numerator / denominator

    @resilient_executor
    def fetch_key(self, key):
        if not isinstance(key, str):
            raise TypeError("Key must be string")
        return self.data[key]

def run_safe_sequence():
    proc = EdgeCaseProcessor({'a': 10})
    results = [
        proc.calculate_ratio(10, 0),
        proc.fetch_key(123),
        proc.fetch_key('a')
    ]
    return [r for r in results if r is not None]

if __name__ == "__main__":
    print(run_safe_sequence())