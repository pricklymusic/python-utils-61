from typing import Any, Callable, Dict, List, TypeVar, Union

T = TypeVar('T')

def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Chain multiple functions together like a pipeline."""
    def pipeline(data: Any) -> Any:
        for func in funcs:
            data = func(data)
        return data
    return pipeline

def partition(predicate: Callable[[T], bool], iterable: List[T]) -> tuple[List[T], List[T]]:
    """Split items into two lists based on boolean filter."""
    true_list, false_list = [], []
    for item in iterable:
        if predicate(item):
            true_list.append(item)
        else:
            false_list.append(item)
    return true_list, false_list

def deep_update(base: Dict[Any, Any], update: Dict[Any, Any]) -> Dict[Any, Any]:
    """Recursively merge dictionaries with priority to update keys."""
    for key, value in update.items():
        if isinstance(value, dict) and key in base and isinstance(base[key], dict):
            deep_update(base[key], value)
        else:
            base[key] = value
    return base

def memoize_once(func: Callable[..., T]) -> Callable[..., T]:
    """A cache wrapper that stores only the last invocation."""
    cache: Dict[str, Union[T, None]] = {'result': None, 'args': None}
    def wrapper(*args: Any) -> T:
        if cache['args'] != args:
            cache['result'] = func(*args)
            cache['args'] = args
        return cache['result'] # type: ignore
    return wrapper