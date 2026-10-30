import collections
from typing import Any, Iterable, Dict, Union

def deep_flatten(items: Iterable[Any]) -> Iterable[Any]:
    """Recursively flatten nested iterables into a stream."""
    for item in items:
        if isinstance(item, (list, tuple, set)):
            yield from deep_flatten(item)
        else:
            yield item

def dict_shredder(data: Dict[Any, Any], separator: str = '.') -> Dict[str, Any]:
    """Flatten nested dictionary keys into dot notation."""
    items = {}
    for key, value in data.items():
        if isinstance(value, dict):
            for sub_key, sub_value in dict_shredder(value, separator).items():
                items[f"{key}{separator}{sub_key}"] = sub_value
        else:
            items[key] = value
    return items

def batch_process(data: Iterable[Any], size: int) -> Iterable[Iterable[Any]]:
    """Generator yielding fixed-size chunks of data."""
    it = iter(data)
    while chunk := list(collections.islice(it, size)):
        yield chunk

def type_coerce(val: Any, target_type: type) -> Any:
    """Graceful type casting with fallback to original."""
    try:
        return target_type(val)
    except (ValueError, TypeError):
        return val