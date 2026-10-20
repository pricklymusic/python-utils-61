import math
import sys
import functools
from typing import Any, Callable, TypeVar, Tuple, Dict

T = TypeVar('T')

class EdgeCaseRegistry:
    """Registry mapping exceptions to fallback transformers for edge case recovery."""
    
    def __init__(self, default_fallback: Any = None):
        self._handlers: Dict[type, Callable[[BaseException, Tuple[Any, ...]], Any]] = {}
        self.default_fallback = default_fallback

    def register(self, *exc_types: type):
        def decorator(fn: Callable):
            for exc in exc_types:
                self._handlers[exc] = fn
            return fn
        return decorator

    def resolve(self, exc: BaseException, *args: Any) -> Any:
        for exc_type, handler in self._handlers.items():
            if isinstance(exc, exc_type):
                return handler(exc, *args)
        if callable(self.default_fallback):
            return self.default_fallback(*args)
        return self.default_fallback


def safe_evaluator(registry: EdgeCaseRegistry):
    """Decorator wrapping functions with edge-case interception logic."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                res = func(*args, **kwargs)
                if isinstance(res, float) and (math.isnan(res) or math.isinf(res)):
                    raise ValueError(f"Unstable numerical result detected: {res}")
                return res
            except Exception as err:
                return registry.resolve(err, *args)
        return wrapper
    return decorator


resilient_dispatcher = EdgeCaseRegistry(default_fallback=lambda *a: None)

@resilient_dispatcher.register(ZeroDivisionError, OverflowError)
def _handle_math_edge_cases(exc: Exception, *args: Any) -> float:
    return float('inf') if isinstance(exc, OverflowError) else 0.0

@resilient_dispatcher.register(RecursionError)
def _handle_recursion_edge_cases(exc: Exception, *args: Any) -> Any:
    sys.setrecursionlimit(min(sys.getrecursionlimit() * 2, 5000))
    return args[0] if args else None

@resilient_dispatcher.register(TypeError, ValueError)
def _handle_type_edge_cases(exc: Exception, *args: Any) -> Any:
    if args and hasattr(args[0], '__str__'):
        return str(args[0])
    return f"recovered_from_{type(exc).__name__}"
