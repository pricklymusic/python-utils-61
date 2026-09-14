import functools
from typing import Callable, Any, Iterable, Tuple, List

class Pipe:
    """A functional pipeline wrapper for sequential data transformations."""
    def __init__(self, value: Any):
        self._value = value

    @property
    def value(self) -> Any:
        return self._value

    def __or__(self, step: Callable[..., Any]) -> "Pipe":
        """Applies a callable to the internal value, returning a new Pipe."""
        if not callable(step):
            raise TypeError(f"Pipeline step must be callable, got {type(step).__name__}")
        return Pipe(step(self._value))

    def __repr__(self) -> str:
        return f"Pipe({self._value!r})"

def select(predicate: Callable[[Any], bool]) -> Callable[[Iterable[Any]], List[Any]]:
    """Generates a filter function using the provided predicate."""
    return lambda items: [item for item in items if predicate(item)]

def modify(transformer: Callable[[Any], Any]) -> Callable[[Iterable[Any]], List[Any]]:
    """Generates a mapping function using the provided transformer."""
    return lambda items: [transformer(item) for item in items]

def split_by(predicate: Callable[[Any], bool]) -> Callable[[Iterable[Any]], Tuple[List[Any], List[Any]]]:
    """Splits an iterable into a tuple of matching and non-matching lists."""
    def _splitter(items: Iterable[Any]) -> Tuple[List[Any], List[Any]]:
        matched, unmatched = [], []
        for item in items:
            (matched if predicate(item) else unmatched).append(item)
        return matched, unmatched
    return _splitter