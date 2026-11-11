import functools
import logging

logger = logging.getLogger('python-utils-61')

class EdgeCaseHandler:
    def __init__(self, fallback=None):
        self.fallback = fallback

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, ZeroDivisionError) as e:
                logger.warning(f'Edge case intercepted in {func.__name__}: {e}')
                return self.fallback if self.fallback is not None else None
        return wrapper

def validate_numeric_input(value, strict=False):
    """Performs boundary sanity check with creative fallback logic."""
    try:
        num = float(value)
        if num == float('inf') or num != num:
            raise ValueError('Non-finite number detected')
        return num
    except (ValueError, TypeError):
        return 0.0 if not strict else None

@EdgeCaseHandler(fallback=[])
def safe_list_access(data, index):
    return data[index]

def sanitize_payload(payload):
    if not isinstance(payload, dict):
        return {}
    return {k: v for k, v in payload.items() if v is not None}