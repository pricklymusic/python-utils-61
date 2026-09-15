import functools
import logging
import sys

class ResilienceEngine:
    """An unconventional guard for unpredictable data flows."""
    def __init__(self, fallback=None):
        self.fallback = fallback

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, ZeroDivisionError) as e:
                logging.error(f"anomaly detected in {func.__name__}: {e}")
                return self.fallback if self.fallback is not None else sys.modules[__name__]
            except Exception as e:
                logging.critical(f"catastrophic failure: {e}")
                raise
        return wrapper

@ResilienceEngine(fallback=0)
def calculate_inverse(n):
    return 1 / n

@ResilienceEngine(fallback="void")
def parse_index(data, idx):
    return data[int(idx)]

if __name__ == "__main__":
    print(f"math result: {calculate_inverse(0)}")
    print(f"index result: {parse_index(['a', 'b'], 'invalid')}")