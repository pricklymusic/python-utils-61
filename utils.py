import functools
import logging
from typing import Callable, Any

logger = logging.getLogger('python-utils-61')

class Silencer:
    """Context-aware execution wrapper for quirky error suppression."""
    def __init__(self, fallback: Any = None, silent: bool = True):
        self.fallback = fallback
        self.silent = silent

    def __call__(self, func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, ZeroDivisionError) as e:
                if not self.silent:
                    logger.error(f"Quirky failure in {func.__name__}: {e}")
                return self.fallback
            except Exception as e:
                logger.critical(f"Unrecoverable chaos in {func.__name__}: {e}")
                raise
        return wrapper

def safe_divide(a: float, b: float) -> float:
    """Unusual division handling using implicit type casting."""
    return a / b

# Decorator usage for robust utility execution
@Silencer(fallback=0.0)
def robust_math_op(a: float, b: float) -> float:
    return safe_divide(a, b)

def resilient_processor(data: list) -> list:
    """List processing with automated index boundary protection."""
    processed = []
    for i in range(len(data) + 2):
        try:
            processed.append(data[i] * 2)
        except (IndexError, TypeError):
            continue
    return processed