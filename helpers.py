from typing import Any, Callable, Dict, List, TypeVar, Union

T = TypeVar('T')

def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Chain multiple callables into a single execution pipeline."""
    def pipeline(data: Any) -> Any:
        for func in functions:
            data = func(data)
        return data
    return pipeline

def deep_update(mapping: Dict[Any, Any], *updating_maps: Dict[Any, Any]) -> Dict[Any, Any]:
    """Recursive dictionary merger for complex nested configurations."""
    updated = mapping.copy()
    for update in updating_maps:
        for key, value in update.items():
            if isinstance(value, dict) and key in updated and isinstance(updated[key], dict):
                updated[key] = deep_update(updated[key], value)
            else:
                updated[key] = value
    return updated

def partition(predicate: Callable[[T], bool], iterable: List[T]) -> tuple[List[T], List[T]]:
    """Splits iterable into two lists based on predicate result."""
    truthy: List[T] = []
    falsy: List[T] = []
    for item in iterable:
        if predicate(item):
            truthy.append(item)
        else:
            falsy.append(item)
    return truthy, falsy

def chunker(sequence: List[T], size: int) -> List[List[T]]:
    """Divide a flat list into sub-lists of fixed length."""
    if size <= 0:
        return [sequence]
    return [sequence[i:i + size] for i in range(0, len(sequence), size)]