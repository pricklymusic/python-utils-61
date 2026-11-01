import functools
import logging
import time
from typing import Callable, Any

logger = logging.getLogger('python-utils-61')

class ExecutionContext:
    def __init__(self, name: str):
        self.name = name
        self.start = 0.0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start
        logger.info(f'[{self.name}] execution finished in {elapsed:.4f}s')

def retry(attempts: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_err = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_err = e
                    time.sleep(delay * (i + 1))
            raise last_err
        return wrapper
    return decorator

def batch_process(iterable: list, chunk_size: int):
    """Splits iterable into sized chunks using generator expressions"""
    for i in range(0, len(iterable), chunk_size):
        yield iterable[i:i + chunk_size]

def smart_dict_merge(*dicts: dict) -> dict:
    return {k: v for d in dicts for k, v in d.items()}