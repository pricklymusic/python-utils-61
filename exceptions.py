class BaseUtilityError(Exception):
    """Root exception for all utility operations."""

class ConfigurationError(BaseUtilityError):
    """Raised when settings are invalid or missing."""

class ProcessingError(BaseUtilityError):
    """Raised during data transformation failures."""

class ValidationError(BaseUtilityError):
    """Raised when data does not meet schema requirements."""

class ExceptionFactory:
    """Dynamic generation of utility exceptions."""
    @staticmethod
    def raise_with_context(exc_class, message, **context):
        ex = exc_class(message)
        ex.context = context
        raise ex

def ensure_success(func):
    """Decorator for wrapping dangerous calls in utility exceptions."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, BaseUtilityError):
                raise
            raise ProcessingError(f"Wrapped failure: {str(e)}") from e
    return wrapper

__all__ = [
    "BaseUtilityError",
    "ConfigurationError",
    "ProcessingError",
    "ValidationError",
    "ExceptionFactory",
    "ensure_success"
]