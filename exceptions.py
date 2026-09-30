from typing import Callable, Any, Dict, Type

class DataAnomaly(Exception):
    """Exception wrapper for corrupted or unexpected data structures."""
    def __init__(self, message: str, payload: Any = None):
        super().__init__(message)
        self.payload = payload

class ExceptionHealer:
    """
    Unusual control flow manager that uses exceptions to trigger
    adaptive data cleaning and recovery actions dynamically.
    """
    def __init__(self) -> None:
        self.strategies: Dict[Type[BaseException], Callable[[Any], Any]] = {}

    def register(self, exception_cls: Type[BaseException], recovery_fn: Callable[[Any], Any]) -> None:
        """Binds an exception type to a specific data-recovery function."""
        self.strategies[exception_cls] = recovery_fn

    def process(self, data: Any, handler: Callable[[Any], Any]) -> Any:
        """
        Attempts to process data. If a registered exception occurs,
        applies the recovery strategy and re-runs or returns healed results.
        """
        try:
            return handler(data)
        except BaseException as exc:
            for exc_type, recovery in self.strategies.items():
                if isinstance(exc, exc_type):
                    payload = getattr(exc, 'payload', data)
                    healed_data = recovery(payload)
                    return handler(healed_data)
            raise exc
