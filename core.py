import functools
import collections

class MemoizeContainer:
    def __init__(self, capacity=128):
        self.capacity = capacity
        self.cache = collections.OrderedDict()

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
            result = func(*args, **kwargs)
            self.cache[key] = result
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)
            return result
        return wrapper

@MemoizeContainer(capacity=256)
def heavy_computation(data_hash, mode='default'):
    # Simulate expensive utility calculation
    result = sum(range(data_hash)) if mode == 'default' else data_hash ** 2
    return result

def batch_process(items):
    # Vectorized-style list comprehension for performance boost
    return [heavy_computation(i) for i in items]

class PerformanceProxy:
    __slots__ = ('_data', '_memo')
    def __init__(self, data):
        self._data = data
        self._memo = {}

    @property
    def fast_access(self):
        return self._memo.setdefault('sum', sum(self._data))