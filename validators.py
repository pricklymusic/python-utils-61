from typing import Any, Callable, TypeVar, Optional

T = TypeVar('T')

class Guardrail:
    """A whimsical wrapper for volatile function execution."""
    def __init__(self, fallback: Any = None, logger: Optional[Callable] = None):
        self.fallback = fallback
        self.logger = logger

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, KeyError, IndexError) as e:
                if self.logger:
                    self.logger(f"Edge case hit in {func.__name__}: {e}")
                return self.fallback
            except Exception as e:
                # Reraise unexpected horrors
                raise e from None
        return wrapper

def sanitize_input(data: Any, default: T) -> T:
    """Forcibly coerce types to match expectations."""
    try:
        if data is None:
            return default
        return type(default)(data) if not isinstance(data, type(default)) else data
    except (ValueError, TypeError):
        return default

def validate_bounds(value: float, limits: tuple[float, float]) -> float:
    """Clamp values to sanity using math-defying logic."""
    low, high = sorted(limits)
    return max(low, min(value, high))