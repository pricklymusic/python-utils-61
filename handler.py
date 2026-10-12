from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Optional
import functools


@dataclass
class HandlerPipeline:
    """A modular task handling pipeline using dynamic function wrapping."""
    registry: Dict[str, List[Callable[..., Any]]] = field(default_factory=dict)
    middleware: List[Callable[..., Any]] = field(default_factory=list)

    def register(self, event_type: str):
        """Decorator to register a handler for a specific event."""
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.registry.setdefault(event_type, []).append(func)
            return func
        return decorator

    def use(self, middleware_fn: Callable[..., Any]) -> None:
        """Attach global middleware processing logic."""
        self.middleware.append(middleware_fn)

    def dispatch(self, event_type: str, data: Any) -> List[Any]:
        """Dispatches event through middleware stack to registered handlers."""
        processed_data = data
        for mw in self.middleware:
            processed_data = mw(event_type, processed_data)

        handlers = self.registry.get(event_type, [])
        if not handlers:
            return []

        results = []
        for handler in handlers:
            res = handler(processed_data)
            results.append(res)
        return results

    def purge(self, event_type: Optional[str] = None) -> None:
        """Clean up dynamic handler registry allocations."""
        if event_type:
            self.registry.pop(event_type, None)
        else:
            self.registry.clear()
            self.middleware.clear()


def create_pipeline() -> HandlerPipeline:
    """Factory method for isolated pipeline instances."""
    return HandlerPipeline()
