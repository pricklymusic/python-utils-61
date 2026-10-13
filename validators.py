import functools
from typing import Callable, Any

class MemoizedValidator:
    __slots__ = ('func', 'cache')

    def __init__(self, func: Callable):
        self.func = func
        self.cache = {}

    def __call__(self, *args: Any) -> bool:
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]

def fast_type_check(target_type: type) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(value: Any) -> bool:
            if not isinstance(value, target_type):
                return False
            return func(value)
        return wrapper
    return decorator

@fast_type_check(int)
def is_positive(n: int) -> bool:
    return n > 0

class ValidatorRegistry:
    _storage = {}

    @classmethod
    def register(cls, name: str, func: Callable):
        cls._storage[name] = MemoizedValidator(func)

    @classmethod
    def validate(cls, name: str, value: Any) -> bool:
        validator = cls._storage.get(name)
        return validator(value) if validator else False

ValidatorRegistry.register('positive', is_positive)