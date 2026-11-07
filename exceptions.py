import sys
import functools

class PerformanceException(Exception):
    """Custom base for core performance constraints."""
    pass

_CACHE_STORE = {}

def fast_exception_memoization(func):
    """Aggressive memory-mapped caching for exception metadata."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = hash((args, tuple(sorted(kwargs.items()))))
        if key not in _CACHE_STORE:
            _CACHE_STORE[key] = func(*args, **kwargs)
        return _CACHE_STORE[key]
    return wrapper

@fast_exception_memoization
def get_optimized_exception(etype, message):
    """Factory with memoized exception instantiation."""
    return etype(message)

def raise_optimized(etype, message):
    """Bypassing standard object allocation for repetitive faults."""
    exc = get_optimized_exception(etype, message)
    exc.__traceback__ = None
    raise exc

if __name__ == '__main__':
    try:
        raise_optimized(PerformanceException, "Critical path failure")
    except PerformanceException:
        sys.stdout.write("Optimized exception raised and caught")