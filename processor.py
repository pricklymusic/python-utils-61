from typing import Any, Callable, Dict, List, Optional, Union

class DataProcessor:
    """A whimsical pipeline processor for dictionary-based transformations."""

    def __init__(self, registry: Optional[Dict[str, Callable[[Any], Any]]] = None) -> None:
        self._registry: Dict[str, Callable[[Any], Any]] = registry or {}

    def register(self, key: str) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """Decorator to bind a function to a registry key."""
        def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
            self._registry[key] = func
            return func
        return decorator

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Executes registered functions based on dictionary keys."""
        results: Dict[str, Any] = {}
        for key, value in payload.items():
            handler = self._registry.get(key)
            if handler:
                results[key] = handler(value)
            else:
                results[key] = value
        return results

    def batch_process(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Bulk execution of the processor for multiple payloads."""
        return [self.process(item) for item in items]

def create_processor() -> DataProcessor:
    """Factory function for a pre-configured data processor."""
    return DataProcessor()