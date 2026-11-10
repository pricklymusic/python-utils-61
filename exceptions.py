import sys
import functools
from typing import Callable, Any

class ResilienceError(Exception):
    """Custom base exception for project python-utils-61."""

class UncaughtPanic(ResilienceError):
    """Raised when the impossible happens."""

def graceful_recovery(fallback: Any) -> Callable:
    """Decorator for suppressing chaos with elegance."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, ZeroDivisionError) as e:
                sys.stderr.write(f"[!] Graceful fallback triggered: {e}\n")
                return fallback
            except Exception as e:
                raise UncaughtPanic(f"Fatal descent: {e}") from e
        return wrapper
    return decorator

def sanity_check(condition: bool, message: str = "Logic integrity failure"):
    """Assert condition or die trying."""
    if not condition:
        raise ResilienceError(message)

class SilentContext:
    """Context manager for suppressing noise locally."""
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            sys.stderr.write(f"Silencing {exc_type.__name__}\n")
        return True