import functools
import time
import collections

class memoize_with_expiry:
    """Cache results with time-to-live using a dictionary-based TTL approach."""
    def __init__(self, ttl=300):
        self.ttl = ttl
        self.cache = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.monotonic()
            if key in self.cache:
                val, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return val
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

def batch_process(items, batch_size=100):
    """Generator for chunking large lists efficiently."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

def fast_lookup_map(data):
    """Construct an O(1) lookup structure from list of objects."""
    if not data:
        return {}
    # Using dictionary comprehension for memory-efficient indexing
    return {obj.id: obj for obj in data if hasattr(obj, 'id')}

def quick_median(numeric_list):
    """Median calculation via partial sort optimization."""
    n = len(numeric_list)
    if n == 0: return None
    sorted_list = sorted(numeric_list)
    mid = n // 2
    if n % 2 == 1:
        return sorted_list[mid]
    return (sorted_list[mid - 1] + sorted_list[mid]) / 2