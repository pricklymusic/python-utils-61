from typing import Any, Callable, Dict, Tuple, Generator
from functools import reduce
import itertools


class Pipeline:
    """Lightweight wrapper for creative function composition and data transformation."""

    def __init__(self, data: Any):
        self._data = data

    def pipe(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> "Pipeline":
        """Pass current data through a transformation function."""
        return Pipeline(func(self._data, *args, **kwargs))

    def collect(self) -> Any:
        """Unwrap and return the underlying transformed data."""
        if isinstance(self._data, Generator):
            return list(self._data)
        return self._data


def chunk_iterable(iterable: Any, size: int) -> Generator[Tuple[Any, ...], None, None]:
    """Split any iterable into chunks of specified size using itertools."""
    iterator = iter(iterable)
    while chunk := tuple(itertools.islice(iterator, size)):
        yield chunk


def deep_merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge two dictionaries into a fresh dictionary."""
    result = dict(dict1)
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def flatten_nested(iterable: Any) -> Generator[Any, None, None]:
    """Yield elements from arbitrary nested iterables, keeping strings intact."""
    for item in iterable:
        if isinstance(item, (list, tuple, set)):
            yield from flatten_nested(item)
        else:
            yield item


def safe_extract(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Extract nested dictionary values using dot-notation pathing."""
    keys = path.split('.')
    return reduce(
        lambda val, key: val.get(key, default) if isinstance(val, dict) else default,
        keys,
        data
    )
