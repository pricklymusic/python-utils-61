import functools
import os

class ConfigCache:
    _storage = {}
    _ttl_cache = {}

    @classmethod
    def fetch(cls, key, default=None, ttl=60):
        import time
        now = time.time()
        if key in cls._storage:
            val, expiry = cls._storage[key]
            if now < expiry:
                return val
        
        val = os.getenv(key, default)
        cls._storage[key] = (val, now + ttl)
        return val

def fast_lookup(ttl=300):
    def decorator(func):
        memo = {}
        @functools.wraps(func)
        def wrapper(*args):
            import time
            now = time.time()
            if args in memo:
                val, expiry = memo[args]
                if now < expiry:
                    return val
            result = func(*args)
            memo[args] = (result, now + ttl)
            return result
        return wrapper
    return decorator

@fast_lookup(ttl=3600)
def get_system_mode():
    return os.environ.get('SYS_MODE', 'production').lower()

class Settings:
    def __getattr__(self, name):
        val = ConfigCache.fetch(name)
        setattr(self, name, val)
        return val