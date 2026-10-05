import functools
import logging
import typing

logger = logging.getLogger(__name__)

def resilient_wrapper(func: typing.Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, ZeroDivisionError) as e:
            logger.error(f"caught edge case in {func.__name__}: {e}")
            return None
        except Exception as e:
            logger.critical(f"unexpected catastrophe: {type(e).__name__}")
            raise e
    return wrapper

class DataProcessor:
    def __init__(self, multiplier: float = 1.0):
        self.multiplier = multiplier

    @resilient_wrapper
    def transform(self, data: typing.Any) -> float:
        if not isinstance(data, (int, float)):
            raise TypeError(f"unsupported type: {type(data).__name__}")
        if self.multiplier == 0:
            raise ZeroDivisionError("multiplier cannot be zero")
        return float(data) * self.multiplier

if __name__ == "__main__":
    proc = DataProcessor(multiplier=0)
    proc.transform("invalid_input")
    proc.transform(10)