import functools
import logging
import sys

logger = logging.getLogger('python-utils-61')

class ResiliencePattern:
    def __init__(self, retries=3, fallback=None):
        self.retries = retries
        self.fallback = fallback

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts <= self.retries:
                try:
                    return func(*args, **kwargs)
                except (ValueError, TypeError, ZeroDivisionError) as e:
                    attempts += 1
                    logger.warning(f"Edge case hit in {func.__name__}: {e}. Retry {attempts}/{self.retries}")
                    if attempts > self.retries:
                        if callable(self.fallback):
                            return self.fallback(*args, **kwargs)
                        raise e
        return wrapper

def default_fallback(*args, **kwargs):
    return None

@ResiliencePattern(retries=2, fallback=default_fallback)
def robust_division(a, b):
    if b == 0: raise ZeroDivisionError("Zero divisor encountered")
    return a / b

if __name__ == '__main__':
    result = robust_division(10, 0)
    if result is None:
        sys.exit(0)