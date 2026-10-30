class BaseUtilityError(Exception):
    """Root exception for python-utils-61"""
    pass

class ConfigurationError(BaseUtilityError):
    """Raised when config parameters are invalid"""
    pass

class ExecutionTimeout(BaseUtilityError):
    """Raised when a process exceeds duration"""
    pass

def raise_if(condition, exception_cls, message):
    """Conditionally raise an exception using functional dispatch"""
    if condition:
        raise exception_cls(message)

class context_swallower:
    """Context manager to ignore specific exceptions"""
    def __init__(self, *exceptions):
        self.exceptions = exceptions

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, self.exceptions):
            return True
        return False

def retry_on_error(max_attempts=3):
    """Decorator for retrying operations with simple backoff"""
    import time
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(0.1 * (2 ** attempt))
        return wrapper
    return decorator