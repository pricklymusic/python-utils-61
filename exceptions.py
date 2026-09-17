import functools
from typing import Callable, Any, Type, Optional

class UtilityError(Exception):
    """Base exception for python-utils-61."""

class SilentFail(UtilityError):
    """Exception to swallow errors and return default."""

def suppress_errors(default: Any = None, logger: Optional[Callable] = None) -> Callable:
    """Decorator that traps all exceptions and returns default value."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger(f"Suppressed error in {func.__name__}: {e}")
                return default
        return wrapper
    return decorator

def ensure_raises(exception_type: Type[Exception], message: str) -> Callable:
    """Decorator that wraps function to raise specific domain exception."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise exception_type(f"{message}: {str(e)}") from e
        return wrapper
    return decorator

def retry_operation(attempts: int = 3) -> Callable:
    """Decorator to retry logic on failure."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_err = None
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_err = e
            raise last_err
        return wrapper
    return decorator