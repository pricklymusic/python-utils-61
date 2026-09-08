import functools
from typing import Callable, Any, Iterable, Generator

class ProcessingError(Exception):
    """Custom exception wrapper for processor edge cases."""
    def __init__(self, message: str, original_cause: Exception = None):
        super().__init__(message)
        self.original_cause = original_cause

def resilient_step(fallback_val: Any = None):
    """Decorator to trap unexpected exceptions and return a fallback value."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (TypeError, ValueError, AttributeError, KeyError):
                return fallback_val
            except Exception as unhandled:
                raise ProcessingError(f"Fatal anomaly in {func.__name__}", original_cause=unhandled) from unhandled
        return wrapper
    return decorator

class SafeBatchProcessor:
    def __init__(self, strict_mode: bool = False):
        self.strict_mode = strict_mode
        self.err_count = 0

    @resilient_step(fallback_val=None)
    def transform_item(self, item: Any) -> dict:
        if item is None:
            raise ValueError("Item cannot be None")
        if isinstance(item, (int, float)):
            return {"val": float(item), "type": "numeric"}
        if isinstance(item, str):
            return {"val": item.strip().lower(), "type": "text"}
        if isinstance(item, dict):
            return {k: str(v) for k, v in item.items() if not k.startswith("_")}
        raise TypeError(f"Unsupported payload type: {type(item)}")

    def process_stream(self, stream: Iterable[Any]) -> Generator[dict, None, None]:
        for idx, element in enumerate(stream):
            try:
                result = self.transform_item(element)
                if result is not None:
                    yield result
                elif self.strict_mode:
                    raise ProcessingError(f"Rejected payload at index {idx}")
            except ProcessingError as pe:
                self.err_count += 1
                if self.strict_mode:
                    raise pe
