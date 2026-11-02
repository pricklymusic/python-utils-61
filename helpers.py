import math
from typing import Any, Callable, Iterable, TypeVar

T = TypeVar("T")

class ResilientEvaluator:
    """Context-based evaluator absorbing edge case exceptions and non-finite floats."""

    def __init__(self, fallback: Any = None, exceptions: tuple[type[BaseException], ...] = (Exception,)):
        self.fallback = fallback
        self.exceptions = exceptions

    def evaluate(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        try:
            val = func(*args, **kwargs)
            if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
                return self.fallback
            return val
        except self.exceptions:
            return self.fallback

def safe_dig(container: Any, path: Iterable[Any], default: Any = None) -> Any:
    """Traverse nested collections safely, handling boundary edge cases."""
    current = container
    evaluator = ResilientEvaluator(fallback=default, exceptions=(TypeError, KeyError, IndexError, ValueError))

    for key in path:
        def _step(c: Any, k: Any) -> Any:
            if isinstance(c, dict):
                return c[k]
            if isinstance(c, (list, tuple, bytes, bytearray)):
                idx = int(k)
                return c[idx]
            return getattr(c, str(k))

        current = evaluator.evaluate(_step, current, key)
        if current is default:
            break
    return current

def coerce_numeric(value: Any, default: float = 0.0, allow_zero: bool = True) -> float:
    """Coerce untrusted inputs to float, guarding against NaN, Inf, and overflow edge cases."""
    evaluator = ResilientEvaluator(fallback=default, exceptions=(ValueError, TypeError, OverflowError))
    res = evaluator.evaluate(lambda v: float(v if not isinstance(v, (bytes, bytearray)) else v.decode("utf-8")), value)
    if not allow_zero and res == 0.0:
        return default
    return res