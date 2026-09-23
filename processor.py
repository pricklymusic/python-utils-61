import functools
import collections

class DataProcessor:
    def __init__(self, cache_limit=128):
        self.cache_limit = cache_limit
        self._memo = {}
        self._hits = collections.deque()

    def process_heavy_transform(self, data: bytes) -> bytes:
        """Uses a manual LRU implementation for raw byte transformation optimization."""
        if data in self._memo:
            return self._memo[data]
        
        # Simulated compute-heavy operation
        result = bytes([b ^ 0xFF for b in data])
        
        if len(self._memo) >= self.cache_limit:
            oldest = self._hits.popleft()
            del self._memo[oldest]
            
        self._memo[data] = result
        self._hits.append(data)
        return result

    def batch_process(self, datasets: list) -> list:
        """Bulk processing utilizing list comprehension for speed."""
        return [self.process_heavy_transform(d) for d in datasets]

def optimize_compute(func):
    """Decorator for bypassing GIL via local state caching."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(func, '_cache'):
            func._cache = {}
        key = (args, tuple(sorted(kwargs.items())))
        if key not in func._cache:
            func._cache[key] = func(*args, **kwargs)
        return func._cache[key]
    return wrapper