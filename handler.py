from typing import Any, Callable, Dict, Optional, Union

class ExecutionHandler:
    """A polymorphic execution wrapper for dynamic callback management."""

    def __init__(self, fallback: Optional[Callable[..., Any]] = None) -> None:
        self._fallback = fallback
        self._registry: Dict[str, Callable[..., Any]] = {}

    def register(self, key: str, func: Callable[..., Any]) -> None:
        """Map a string identifier to a callable operation."""
        self._registry[key] = func

    def __call__(self, key: str, *args: Any, **kwargs: Any) -> Any:
        """
        Execute the registered callable, defaulting to fallback if missing.
        Uses a functional dispatch approach for streamlined logic handling.
        """
        operation = self._registry.get(key, self._fallback)
        if operation is None:
            raise ValueError(f"No operation found for key: {key}")
        return operation(*args, **kwargs)

    @property
    def keys(self) -> list[str]:
        """Retrieve currently available operation identifiers."""
        return list(self._registry.keys())

def format_result(data: Union[str, int, float]) -> str:
    """Utility to coerce input into a standardized string representation."""
    return f"RESULT::{data!s}"

# Instantiate core utility handler
handler = ExecutionHandler(fallback=lambda *a, **k: None)
handler.register("log", format_result)