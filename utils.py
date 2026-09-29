import functools
import logging
from typing import Any, Callable, TypeVar, ParamSpec

P = ParamSpec('P')
R = TypeVar('R')

class ResilienceDecorator:
    def __init__(self, retries: int = 3, default: Any = None):
        self.retries = retries
        self.default = default

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            attempt = 0
            while attempt <= self.retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt > self.retries:
                        logging.error(f'Exhausted retries for {func.__name__}: {e}')
                        return self.default
                    logging.warning(f'Retrying {func.__name__} (attempt {attempt})')
            return self.default
        return wrapper

def safe_execute(func: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R | None:
    try:
        return func(*args, **kwargs)
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logging.debug(f'Silencing expected edge case error: {e}')
        return None

@ResilienceDecorator(retries=2, default={})
def fetch_data_robust(source: str) -> dict:
    if not source:
        raise ValueError('Source cannot be empty')
    return {'status': 'success', 'source': source}