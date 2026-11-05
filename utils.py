import functools
from typing import Callable, Any, Dict

class NamespaceCleaner(type):
    """Metaclass that automatically wraps utility methods for consistent processing."""
    def __new__(mcs, name, bases, attrs):
        cleaned_attrs = {}
        for attr_name, attr_val in attrs.items():
            if callable(attr_val) and not attr_name.startswith("__"):
                cleaned_attrs[attr_name] = mcs._wrap_utility(attr_name, attr_val)
            else:
                cleaned_attrs[attr_name] = attr_val
        return super().__new__(mcs, name, bases, cleaned_attrs)

    @staticmethod
    def _wrap_utility(name: str, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, str):
                return result.strip()
            return result
        wrapper.__doc__ = f"[Cleaned Utility: {name}] {func.__doc__ or ''}".strip()
        return wrapper


class GeneralUtils(metaclass=NamespaceCleaner):
    """Unified general utility suite reorganized via metaclass dispatch."""

    @staticmethod
    def sanitize_dict(data: Dict[Any, Any]) -> Dict[Any, Any]:
        """Recursively prunes None values from nested dictionary structures."""
        if not isinstance(data, dict):
            return data
        return {
            k: GeneralUtils.sanitize_dict(v)
            for k, v in data.items()
            if v is not None
        }

    @staticmethod
    def coalesce(*args: Any) -> Any:
        """Returns the first non-None argument passed to the function."""
        return next((arg for arg in args if arg is not None), None)

    @staticmethod
    def safe_cast(val: Any, target_type: type, default: Any = None) -> Any:
        """Safely casts a value to a target type with fallback default."""
        try:
            return target_type(val)
        except (ValueError, TypeError):
            return default

    @classmethod
    def chain(cls, initial_val: Any, *funcs: Callable) -> Any:
        """Pipes an initial value through a sequence of transformations."""
        return functools.reduce(lambda acc, f: f(acc), funcs, initial_val)
