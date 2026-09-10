import sys
import warnings
from typing import Callable, Type, Any, Union, Tuple, Dict

_DYNAMIC_EXCEPTIONS: Dict[str, Type[Exception]] = {}

def get_dynamic_exception(name: str, base_class: Type[Exception] = Exception) -> Type[Exception]:
    """Dynamically spawns and caches a custom exception type on the fly."""
    if name not in _DYNAMIC_EXCEPTIONS:
        _DYNAMIC_EXCEPTIONS[name] = type(name, (base_class,), {
            "__doc__": f"Dynamically generated exception: {name}"
        })
    return _DYNAMIC_EXCEPTIONS[name]

class ResilientBoundary:
    """
    A hybrid context manager and decorator that intercepts exceptions
    and either falls back to a default value, warns, or executes a fallback callback.
    """
    def __init__(
        self,
        exceptions: Union[Type[BaseException], Tuple[Type[BaseException], ...]] = Exception,
        fallback: Any = None,
        warn_instead: bool = False
    ):
        self.exceptions = exceptions
        self.fallback = fallback
        self.warn_instead = warn_instead

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, self.exceptions):
            if self.warn_instead:
                warnings.warn(f"Suppressed exception in boundary: {exc_val}", category=UserWarning)
            return True
        return False

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except self.exceptions as e:
                if self.warn_instead:
                    warnings.warn(f"Function {func.__name__} raised error: {e}", category=UserWarning)
                if callable(self.fallback):
                    return self.fallback(e)
                return self.fallback
        return wrapper

def try_or_default(func: Callable, *args, default: Any = None, **kwargs) -> Any:
    """Evaluates a target callable, absorbing any exception and returning a default value."""
    try:
        return func(*args, **kwargs)
    except Exception:
        return default
