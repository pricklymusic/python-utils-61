import functools
import logging
import time
from typing import Callable, Any

logger = logging.getLogger('python-utils-61')

class ExecutionContext:
    def __init__(self, retries: int = 3, delay: float = 0.5):
        self.retries = retries
        self.delay = delay

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            while attempts < self.retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logger.warning(f"Attempt {attempts} failed: {e}")
                    if attempts >= self.retries:
                        raise
                    time.sleep(self.delay * attempts)
            return None
        return wrapper

def batch_process(items: list, chunk_size: int = 10):
    """generator for functional data chunking"""
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

def clean_runtime_environment(scope: dict):
    """wipes temporary variables from current scope"""
    keys = [k for k in scope if k.startswith('tmp_')]
    for k in keys:
        del scope[k]
    return len(keys)