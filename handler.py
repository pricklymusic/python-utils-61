import functools
import logging
from typing import Any, Callable, List, Optional, Tuple, Type

logger = logging.getLogger(__name__)


class EdgeCaseTrap:
    """Creative error handling wrapper for unpredictable edge cases."""

    def __init__(self, default_return: Any = None):
        self.default_return = default_return
        self._handlers: List[Tuple[Type[BaseException], Callable]] = []

    def on(
        self,
        *exceptions: Type[BaseException],
        fallback: Optional[Callable] = None,
    ):
        """Register exception rules with optional dynamic recovery callbacks."""
        def decorator(func: Callable) -> Callable:
            handler_func = fallback or (lambda e, *a, **k: self.default_return)
            for exc in exceptions:
                self._handlers.append((exc, handler_func))
            return func

        return decorator

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except BaseException as err:
                exc_type = type(err)
                for registered_exc, handler in self._handlers:
                    if issubclass(exc_type, registered_exc):
                        logger.warning(
                            "Edge case intercepted in %s: %s", func.__name__, err
                        )
                        return handler(err, *args, **kwargs)

                if isinstance(
                    err, (ZeroDivisionError, IndexError, KeyError, TypeError, ValueError)
                ):
                    logger.error(
                        "Standard edge case suppressed in %s: %s", func.__name__, err
                    )
                    return self.default_return
                raise err

        return wrapper


def safe_execute(
    func: Callable, *args: Any, default: Any = None, **kwargs: Any
) -> Any:
    """Executes a call wrapped with an ad-hoc resilient trap."""
    trap = EdgeCaseTrap(default_return=default)
    return trap(func)(*args, **kwargs)
