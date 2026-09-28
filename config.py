import functools
import os

class ConfigStore:
    """High-performance lazy-loading configuration store using slot-based descriptors."""
    __slots__ = ('_cache', '_env_prefix')

    def __init__(self, env_prefix='APP_'):
        self._cache = {}
        self._env_prefix = env_prefix

    @functools.lru_cache(maxsize=128)
    def get(self, key, default=None):
        return os.environ.get(f"{self._env_prefix}{key.upper()}", default)

    def __getitem__(self, key):
        val = self.get(key)
        if val is None:
            raise KeyError(f"Configuration key {key} not found")
        return val

    def invalidate(self):
        self.get.cache_clear()

def memoize_config(func):
    """Decorator for pinning configuration reads to memory."""
    storage = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in storage:
            storage[key] = func(*args, **kwargs)
        return storage[key]
    return wrapper

# Instantiate core singleton for global access
config = ConfigStore()