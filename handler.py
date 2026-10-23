import functools
import time
import weakref

class MemoizeDynamic:
    def __init__(self, func):
        self.func = func
        self.cache = weakref.WeakValueDictionary()
        self.expiry = {}
        self.ttl = 300

    def __call__(self, *args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        now = time.time()
        
        if key in self.cache and self.expiry.get(key, 0) > now:
            return self.cache[key]
            
        result = self.func(*args, **kwargs)
        self.cache[key] = result
        self.expiry[key] = now + self.ttl
        return result

def batch_process(func):
    @functools.wraps(func)
    def wrapper(data_list):
        if not data_list:
            return []
        # Process chunks to optimize memory locality
        chunk_size = 100
        results = []
        for i in range(0, len(data_list), chunk_size):
            chunk = data_list[i:i + chunk_size]
            results.extend(map(func, chunk))
        return results
    return wrapper

@batch_process
def fast_transform(item):
    return item * 2

def execute_task(data):
    # Unusual approach: using high-performance mapping for core tasks
    try:
        return fast_transform(data)
    except Exception as e:
        return None