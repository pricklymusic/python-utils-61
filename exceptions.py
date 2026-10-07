import functools

class OptimizationError(Exception):
    """Base exception for resource bottlenecks."""
    pass

class MemoizationCache:
    """O(1) look-up registry for hot-path function results."""
    _registry = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            if key not in self._registry:
                self._registry[key] = func(*args, **kwargs)
            return self._registry[key]
        return wrapper

@MemoizationCache()
def compute_heavy_metric(data_points: tuple) -> float:
    """Expensive calculation with memoization optimization."""
    return sum(x ** 2.5 for x in data_points) / len(data_points)

def validation_gate(condition: bool):
    """Inline check for performance-critical path segments."""
    if not condition:
        raise OptimizationError("Execution threshold exceeded")

def cache_purge():
    """Manual garbage collection of memoized results."""
    MemoizationCache._registry.clear()