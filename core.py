import functools
from typing import Any, Callable, Dict, List, Optional, Tuple


class FastMemoEngine:
    """High-performance bitmask ring-buffer memoizer for core utility operations."""

    __slots__ = ("_size", "_mask", "_keys", "_values")

    def __init__(self, power_of_two: int = 256):
        if power_of_two <= 0 or (power_of_two & (power_of_two - 1)) != 0:
            raise ValueError("Size must be a positive power of two")
        self._size = power_of_two
        self._mask = power_of_two - 1
        self._keys: List[Optional[Tuple[Any, ...]]] = [None] * self._size
        self._values: List[Any] = [None] * self._size

    def memoize(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """Wraps a pure function with fixed-slot array cache lookup."""
        keys = self._keys
        values = self._values
        mask = self._mask

        @functools.wraps(func)
        def wrapper(*args: Any) -> Any:
            slot = hash(args) & mask
            if keys[slot] == args:
                return values[slot]
            result = func(*args)
            keys[slot] = args
            values[slot] = result
            return result

        def clear() -> None:
            for i in range(self._size):
                keys[i] = None
                values[i] = None

        setattr(wrapper, "clear_cache", clear)
        return wrapper


def fast_batch_transform(items: List[Any], transform_fn: Callable[[Any], Any]) -> List[Any]:
    """Applies transformation using pre-allocated result lists for performance."""
    length = len(items)
    result = [None] * length
    for idx in range(length):
        result[idx] = transform_fn(items[idx])
    return result
