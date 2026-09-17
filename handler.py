from typing import Callable, Any, Dict, Optional
import functools

class DataHandler:
    """An unconventional handler that treats data as callable flow."""
    
    def __init__(self, processors: Optional[Dict[str, Callable[[Any], Any]]] = None) -> None:
        self._processors: Dict[str, Callable[[Any], Any]] = processors or {}

    def __call__(self, key: str, value: Any) -> Any:
        """Process data using a registered pipeline stage."""
        processor = self._processors.get(key, lambda x: x)
        return processor(value)

    def register(self, key: str) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """Decorator registration for custom pipeline logic."""
        def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
            self._processors[key] = func
            return func
        return decorator

    def pipeline(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply processing pipeline to entire data set."""
        return {k: self(k, v) for k, v in data.items()}

@functools.lru_cache(maxsize=32)
def get_default_handler() -> DataHandler:
    """Factory for standardized data handling instances."""
    return DataHandler()