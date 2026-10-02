import functools
from typing import Any, Callable

class flow:
    """
    A monadic wrapper for safe, fluid extraction and transformation
    of nested data structures with fallbacks.
    """
    def __init__(self, value: Any):
        self._value = value

    def __getitem__(self, key: Any) -> "flow":
        if self._value is None:
            return self
        try:
            return flow(self._value[key])
        except (TypeError, KeyError, IndexError):
            return flow(None)

    def __getattr__(self, name: str) -> "flow":
        if self._value is None:
            return self
        if isinstance(self._value, dict) and name in self._value:
            return flow(self._value[name])
        try:
            return flow(getattr(self._value, name))
        except AttributeError:
            return flow(None)

    def __or__(self, default: Any) -> Any:
        """Provide fallback value: flow(data)['key'] | 'default'"""
        return default if self._value is None else self._value

    def __rshift__(self, func: Callable[[Any], Any]) -> "flow":
        """Transform the inner value: flow(5) >> (lambda x: x * 2)"""
        if self._value is None:
            return self
        try:
            return flow(func(self._value))
        except Exception:
            return flow(None)

    def resolve(self) -> Any:
        """Extract the raw wrapped value directly."""
        return self._value


def pluck(data: Any, path: str, default: Any = None) -> Any:
    """
    Plucks deeply nested attributes or dict keys using a dot-separated string.
    Example: pluck(user_dict, 'profile.address.zip', '00000')
    """
    current = flow(data)
    for part in path.split("."):
        if part.isdigit():
            current = current[int(part)]
        else:
            current = current[part]
    return current | default