import functools
import time

class MemoizeCache:
    def __init__(self, ttl_seconds=60):
        self.cache = {}
        self.ttl = ttl_seconds

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.time()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return result
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

    def purge(self):
        self.cache.clear()

class FastBuffer:
    def __init__(self, chunk_size=1024):
        self.buffer = []
        self.chunk_size = chunk_size

    def push(self, data):
        self.buffer.append(data)
        if len(self.buffer) >= self.chunk_size:
            return self.flush()
        return None

    def flush(self):
        output = "".join(self.buffer)
        self.buffer = []
        return output

def batch_process(iterable, n):
    iterator = iter(iterable)
    while True:
        batch = [next(iterator) for _ in range(n)]
        if not batch:
            break
        yield batch