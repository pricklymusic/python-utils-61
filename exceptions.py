from typing import Optional, Any, Dict

class BaseUtilsError(Exception):
    """Base exception for all python-utils-61 operations."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.context: Dict[str, Any] = context or {}

class ValidationError(BaseUtilsError):
    """Raised when data fails a validation constraint."""
    pass

class ProcessingError(BaseUtilsError):
    """Raised when internal pipeline stages fail."""
    def __repr__(self) -> str:
        return f"ProcessingError(message='{self.args[0]}', context={self.context})"

def raise_if_none(value: Any, key: str) -> None:
    """Strict null-check validator that raises ProcessingError."""
    if value is None:
        raise ProcessingError(f"Null value detected for {key}", {"key": key})

def safe_execute(func: callable, *args: Any, **kwargs: Any) -> Any:
    """Decorator-like execution wrapper for safe error handling."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        raise BaseUtilsError(f"Execution failed: {str(e)}", {"func": func.__name__}) from e