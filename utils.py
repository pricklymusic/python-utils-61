from typing import Any, Callable, Dict, List, TypeVar, Optional

T = TypeVar('T')

def batch_process(data: List[T], size: int = 10) -> List[List[T]]:
    """Splits a list into chunks of fixed size using list comprehension magic."""
    return [data[i:i + size] for i in range(0, len(data), size)]

def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Functional pipe for chaining functions into a single pipeline."""
    def inner(arg: Any) -> Any:
        result = arg
        for f in funcs:
            result = f(result)
        return result
    return inner

def safe_get(data: Dict[Any, Any], keys: List[Any], default: Optional[Any] = None) -> Any:
    """Deep navigation of nested dictionaries with graceful fallback."""
    current = data
    try:
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError, IndexError):
        return default

def toggle_bool(val: bool) -> bool:
    """Inverse state switcher for rapid logical toggling."""
    return not val