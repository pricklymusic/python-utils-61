import functools
import collections

def memoize_with_ttl(ttl_seconds=300):
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            import time
            now = time.time()
            if key in cache:
                val, timestamp = cache[key]
                if now - timestamp < ttl_seconds:
                    return val
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

class FastProcessor:
    """High-performance data transformation utility"""
    def __init__(self, storage=None):
        self._storage = storage or collections.deque(maxlen=1000)

    def bulk_transform(self, data_list, func):
        """Parallel-friendly mapping wrapper"""
        return list(map(func, data_list))

    def get_optimized_batch(self, items):
        """Generator-based batch processing"""
        for i in range(0, len(items), 100):
            yield items[i:i + 100]

    @staticmethod
    def recursive_flatten(container):
        for i in container:
            if isinstance(i, (list, tuple)):
                yield from FastProcessor.recursive_flatten(i)
            else:
                yield i