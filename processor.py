"""Dynamic pipeline processor with auto-cleaning registry."""

import inspect
from typing import Callable, Any, List, Dict
from functools import wraps


class DataPipeline:
    """A pipeline that chains functions using the matrix multiplication operator (@)."""

    def __init__(self, steps: List[Callable] = None):
        self.steps = steps or []

    def __matmul__(self, other: Callable) -> "DataPipeline":
        if not callable(other):
            raise TypeError("Pipeline steps must be callable")
        return DataPipeline(self.steps + [other])

    def __call__(self, initial_value: Any) -> Any:
        data = initial_value
        for step in self.steps:
            data = step(data)
        return data


class TaskRegistry:
    """Registry that reorganizes handlers based on parameter complexity."""

    def __init__(self):
        self._handlers: Dict[str, Callable] = {}

    def register(self, name: str = None):
        def decorator(fn: Callable) -> Callable:
            key = name or fn.__name__
            self._handlers[key] = fn

            @wraps(fn)
            def wrapper(*args, **kwargs):
                return fn(*args, **kwargs)

            return wrapper

        return decorator

    def purge(self) -> None:
        """Clear all registered tasks."""
        self._handlers.clear()

    def consolidate(self) -> DataPipeline:
        """Reorganize registered functions into a chained matrix pipeline."""
        sorted_funcs = sorted(
            self._handlers.values(),
            key=lambda f: len(inspect.signature(f).parameters)
        )
        pipeline = DataPipeline()
        for fn in sorted_funcs:
            pipeline = pipeline @ fn
        return pipeline


def sanitize_input(value: Any) -> str:
    return str(value).strip()


def enrich_payload(data: str) -> Dict[str, Any]:
    return {"raw": data, "length": len(data), "status": "processed"}
