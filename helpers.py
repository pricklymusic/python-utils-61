import functools
from typing import Any, Callable, Type, Union, Tuple

class SafeLookup:
    """A wrapper enabling dynamic dot-notation and safe nested queries on dicts and objects.
    
    Example:
        data = {'users': [{'profile': {'email': 'test@example.com'}}]}
        SafeLookup(data).users[0].profile.email.unwrap('no-email')
    """
    def __init__(self, obj: Any):
        self._obj = obj

    def __getattr__(self, name: str) -> 'SafeLookup':
        if self._obj is None:
            return SafeLookup(None)
        try:
            val = self._obj[name]
        except (KeyError, TypeError, IndexError):
            val = getattr(self._obj, name, None)
        return SafeLookup(val)

    def __getitem__(self, key: Any) -> 'SafeLookup':
        if self._obj is None:
            return SafeLookup(None)
        try:
            return SafeLookup(self._obj[key])
        except (KeyError, TypeError, IndexError):
            return SafeLookup(None)

    def unwrap(self, fallback: Any = None) -> Any:
        """Unwraps the underlying value, returning fallback if None."""
        return self._obj if self._obj is not None else fallback

    def __repr__(self) -> str:
        return f"SafeLookup({self._obj!r})"


def coalesce(*args: Any) -> Any:
    """Returns the first non-None argument, or None if all are None."""
    return next((arg for arg in args if arg is not None), None)


def suppress(exception_type: Union[Type[BaseException], Tuple[Type[BaseException], ...]] = Exception, default: Any = None) -> Callable:
    """Decorator to suppress specific exceptions and return a default value instead."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except exception_type:
                return default
        return wrapper
    return decorator
