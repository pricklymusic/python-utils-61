import functools
import time

class MemoizedProcess:
    def __init__(self, func):
        self.func = func
        self.cache = {}
        self.expiry = {}

    def __call__(self, *args, ttl=300):
        now = time.time()
        if args in self.cache and now < self.expiry.get(args, 0):
            return self.cache[args]
        
        result = self.func(*args)
        self.cache[args] = result
        self.expiry[args] = now + ttl
        return result

def batch_process(items, func, chunk_size=100):
    for i in range(0, len(items), chunk_size):
        yield [func(x) for x in items[i:i + chunk_size]]

@MemoizedProcess
def heavy_computation(data):
    # Simulate expensive transformation
    return sum(pow(x, 2) for x in data if x % 2 == 0)

def optimized_pipeline(data_stream):
    """
    Core execution path using batching and memoization.
    """
    processed = []
    for batch in batch_process(data_stream, lambda x: x, chunk_size=50):
        res = heavy_computation(tuple(batch))
        processed.append(res)
    return processed