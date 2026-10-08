import functools
import logging
from typing import Callable, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('python-utils-61')

class Chainable:
    def __init__(self, value: Any):
        self._v = value

    def pipe(self, func: Callable[[Any], Any]) -> 'Chainable':
        return Chainable(func(self._v))

    def result(self) -> Any:
        return self._v

def retry_on_failure(retries: int = 3):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    logger.warning(f'attempt {i+1} failed: {e}')
            raise last_ex
        return wrapper
    return decorator

def sanitize_dict(data: dict) -> dict:
    return {str(k).strip(): (v.strip() if isinstance(v, str) else v) for k, v in data.items()}

def compose(*functions):
    return lambda x: functools.reduce(lambda v, f: f(v), functions, x)