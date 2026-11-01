"""Dynamic key-value transformation utilities with monadic chaining."""

from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar

T = TypeVar("T")


class LazyTransformer:
    """Wraps dictionary data allowing lazy, chained functional transformations.

    Attributes:
        _data: The underlying initial data dictionary.
        _ops: Queue of transformation functions to apply lazily.
    """

    def __init__(self, data: Optional[Dict[Any, Any]] = None) -> None:
        self._data: Dict[Any, Any] = dict(data) if data else {}
        self._ops: List[Callable[[Dict[Any, Any]], Dict[Any, Any]]] = []

    def pipe(self, fn: Callable[[Dict[Any, Any]], Dict[Any, Any]]) -> "LazyTransformer":
        """Appends a transformation function to the lazy execution pipeline."""
        self._ops.append(fn)
        return self

    def __rshift__(self, fn: Callable[[Dict[Any, Any]], Dict[Any, Any]]) -> "LazyTransformer":
        """Overloads the `>>` operator to support pipe syntax."""
        return self.pipe(fn)

    def evaluate(self) -> Dict[Any, Any]:
        """Executes all queued transformations sequentially and returns the result."""
        result = dict(self._data)
        for op in self._ops:
            result = op(result)
        return result


def flatten_dict(
    d: Dict[str, Any], parent_key: str = "", sep: str = "."
) -> Dict[str, Any]:
    """Flattens a deeply nested dictionary into a single-level key representation.

    Args:
        d: Target nested dictionary.
        parent_key: Key path prefix used during recursion.
        sep: Delimiter for joining nested key strings.

    Returns:
        Flattened dictionary mapping composite keys to values.
    """
    items: List[Tuple[str, Any]] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def sanitize_keys(
    caster: Callable[[str], str] = str.lower
) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """Returns a function that transforms dictionary keys using the given caster."""

    def _transform(d: Dict[str, Any]) -> Dict[str, Any]:
        return {caster(str(k)): v for k, v in d.items()}

    return _transform
