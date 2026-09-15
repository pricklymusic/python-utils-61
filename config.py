import functools
import os
import threading

class ConfigStore:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ConfigStore, cls).__new__(cls)
                cls._instance._data = {}
            return cls._instance

    def __getitem__(self, key):
        return self._data.get(key)

    def __setitem__(self, key, value):
        self._data[key] = value

def memoize_config(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize_config
def get_environment_variable(key: str, default=None):
    val = os.getenv(key, default)
    return val if val is not None else default

def lazy_load_settings(func):
    storage = {}
    def inner():
        if 'result' not in storage:
            storage['result'] = func()
        return storage['result']
    return inner

@lazy_load_settings
def load_defaults():
    return {
        'DEBUG': False,
        'TIMEOUT': 30,
        'RETRIES': 3
    }