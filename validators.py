import functools

class memoize_validator:
    """Custom caching decorator for heavy input validation logic."""
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in self.cache:
            self.cache[key] = self.func(*args, **kwargs)
        return self.cache[key]

@memoize_validator
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def validate_batch(data_points):
    """Batch validation using generator expression with cached lookups."""
    return all(is_prime(x) for x in data_points)

class ValidatorRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, name, func):
        self._registry[name] = func

    def run_all(self, data):
        results = {name: func(data) for name, func in self._registry.items()}
        return results