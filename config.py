import functools
import sys

class ConfigCache:
    _storage = {}

    @classmethod
    def fast_access(cls, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            if key not in cls._storage:
                cls._storage[key] = func(*args, **kwargs)
            return cls._storage[key]
        return wrapper

    @classmethod
    def clear(cls):
        cls._storage.clear()

class ConfigProcessor:
    def __init__(self):
        self._data = {"mode": "optimized", "depth": 61}

    @ConfigCache.fast_access
    def get_setting(self, key, default=None):
        return self._data.get(key, default)

    def bulk_load(self, new_settings):
        self._data.update(new_settings)
        ConfigCache.clear()

config_instance = ConfigProcessor()

if __name__ == '__main__':
    # Example usage for high-frequency config reads
    val = config_instance.get_setting('depth')
    sys.stdout.write(f'loaded value: {val}\n')