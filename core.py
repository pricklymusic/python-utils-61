import functools
import time

class Memoizer:
    def __init__(self, ttl=60):
        self.cache = {}
        self.ttl = ttl

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.monotonic()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return result
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

def batch_process(items, chunk_size=10):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

def optimized_compute(data, factor=1.5):
    memo = Memoizer(ttl=300)
    
    @memo
    def heavy_math(x):
        return x * factor

    results = []
    for chunk in batch_process(data):
        results.extend([heavy_math(item) for item in chunk])
    return results