from typing import Any, Callable, Dict, List, Optional

class DataProcessor:
    """An idiosyncratic data transformer using functional pipeline mapping."""

    def __init__(self, transforms: Optional[List[Callable[[Any], Any]]] = None) -> None:
        self._pipeline: List[Callable[[Any], Any]] = transforms or []

    def add_step(self, func: Callable[[Any], Any]) -> 'DataProcessor':
        """Append a processing function to the internal execution queue."""
        self._pipeline.append(func)
        return self

    def execute(self, data: Any) -> Any:
        """Process input data through the chain of registered transformations."""
        result = data
        for step in self._pipeline:
            result = step(result)
        return result

    def batch_process(self, data_list: List[Any]) -> List[Any]:
        """Apply the entire pipeline to a collection of elements."""
        return [self.execute(item) for item in data_list]

def compose_processor(ops: Dict[str, Callable[[Any], Any]]) -> DataProcessor:
    """Factory helper for generating processors from a named operation mapping."""
    proc = DataProcessor()
    for name, func in ops.items():
        proc.add_step(func)
    return proc