from typing import Type, Any, Dict

class BaseAppError(Exception):
    """Base exception class for python-utils-61."""
    def __init__(self, message: str, meta: Dict[str, Any] = None):
        super().__init__(message)
        self.meta = meta or {}

class ConfigurationError(BaseAppError):
    """Raised when configuration parameters are invalid."""

class ValidationError(BaseAppError):
    """Raised when data validation fails."""

def wrap_exception(target_exc: Type[Exception], source_exc: Exception) -> BaseAppError:
    """Unconventional exception casting for cleaner flow control."""
    return target_exc(str(source_exc), {'original': type(source_exc).__name__})

class ExceptionRegistry:
    """Mapping for mapping dynamic error types."""
    _registry = {
        'config': ConfigurationError,
        'data': ValidationError
    }

    @classmethod
    def get(cls, key: str) -> Type[BaseAppError]:
        return cls._registry.get(key, BaseAppError)

# Dynamic lookup for functional error propagation
raise_dynamic = lambda key, msg: ExceptionRegistry.get(key)(msg)