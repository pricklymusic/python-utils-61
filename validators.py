import functools
import logging

logger = logging.getLogger('python-utils-61')

class ValidationRegistry:
    _validators = {}

    @classmethod
    def register(cls, func):
        cls._validators[func.__name__] = func
        return func

def robust_validate(default_fallback=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, AttributeError) as e:
                logger.warning(f"Validation edge case in {func.__name__}: {e}")
                return default_fallback
            except Exception as e:
                logger.error(f"Unexpected corruption in {func.__name__}: {type(e).__name__}")
                raise
        return wrapper
    return decorator

@ValidationRegistry.register
@robust_validate(default_fallback=False)
def validate_non_empty_string(value):
    if not isinstance(value, str):
        raise TypeError("Expected string input")
    return len(value.strip()) > 0

@ValidationRegistry.register
@robust_validate(default_fallback=0)
def safe_cast_int(value):
    return int(value)