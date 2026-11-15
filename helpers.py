import functools
from typing import Any, Callable, Dict, List, Union

def morph_data(data: Any, transformer: Callable[[Any], Any] = None) -> Any:
    """Recursively traverse structures and apply transformations if provided."""
    if isinstance(data, dict):
        return {str(k): morph_data(v, transformer) for k, v in data.items()}
    elif isinstance(data, (list, tuple, set)):
        return [morph_data(i, transformer) for i in data]
    return transformer(data) if transformer else data

def pipeline(data: Any, *funcs: Callable[[Any], Any]) -> Any:
    """Functional chain execution for arbitrary data transformations."""
    return functools.reduce(lambda d, f: f(d), funcs, data)

def pluck(data: List[Dict], key: str, default: Any = None) -> List[Any]:
    """Extract specific keys from a list of dictionaries."""
    return [d.get(key, default) for d in data if isinstance(d, dict)]

def batch_process(items: List[Any], size: int = 10):
    """Generator for chunking collections into smaller batches."""
    for i in range(0, len(items), size):
        yield items[i:i + size]

def smart_flatten(nested: List[Any]) -> List[Any]:
    """Flatten nested lists using a depth-first traversal."""
    flat = []
    for item in nested:
        if isinstance(item, (list, tuple)):
            flat.extend(smart_flatten(item))
        else:
            flat.append(item)
    return flat