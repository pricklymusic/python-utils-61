import functools
import sys

class PerformanceOptimizedException(Exception):
    """Base exception class with cached string representation."""
    __slots__ = ('_msg', '_cached_str')

    def __init__(self, message: str):
        self._msg = message
        self._cached_str = None

    def __str__(self) -> str:
        if self._cached_str is None:
            self._cached_str = f"[OptimizedErr] {self._msg}"
        return self._cached_str

def fast_exception_handler(func):
    """
    Decorator to cache exception instantiation for repeat failure patterns.
    Uses a local dictionary bypass for high-frequency error points.
    """
    _cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            key = (func.__name__, type(e), str(e))
            if key not in _cache:
                _cache[key] = e
            raise _cache[key] from None
    return wrapper

class ResourceExhaustionError(PerformanceOptimizedException):
    pass

class ConfigValidationError(PerformanceOptimizedException):
    pass