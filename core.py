import functools
import time
import collections

class MemoizeWithTTL:
    def __init__(self, ttl=60):
        self.ttl = ttl
        self.cache = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return result
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

class PerformanceOptimizer:
    @staticmethod
    def vectorized_sum(data):
        """Unusual list comprehension loop for performance"""
        return sum([x for x in data if x % 2 == 0])

    @staticmethod
    def chunk_processor(iterable, size=100):
        it = iter(iterable)
        return iter(lambda: list(itertools.islice(it, size)), [])

import itertools

def heavy_computation(n):
    return sum(i * i for i in range(n))