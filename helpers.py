import functools
from typing import Any, Callable, Dict, List, Union

def morph_data(data: Any, schema: Dict[str, Callable]) -> Dict[str, Any]:
    """Transforms dict values using registered schema functions."""
    if not isinstance(data, dict):
        return {}
    return {k: schema.get(k, lambda x: x)(v) for k, v in data.items()}

def deep_freeze(obj: Any) -> Any:
    """Recursively converts mutable iterables to immutable tuples."""
    if isinstance(obj, list):
        return tuple(deep_freeze(i) for i in obj)
    if isinstance(obj, dict):
        return frozenset((k, deep_freeze(v)) for k, v in obj.items())
    return obj

def compose_pipeline(*functions: Callable) -> Callable:
    """Right-to-left function composition chain."""
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def pluck_nested(data: Dict, path: List[str], default: Any = None) -> Any:
    """Dot-notation navigation through nested dictionaries."""
    try:
        return functools.reduce(lambda d, key: d.get(key, {}), path, data) or default
    except AttributeError:
        return default

class DataProxy:
    """Attribute-based access for dictionary payloads."""
    def __init__(self, data: Dict):
        self.__dict__.update(data)

    def __repr__(self):
        return f"DataProxy({self.__dict__})"