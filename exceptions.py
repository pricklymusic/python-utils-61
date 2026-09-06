class BaseUtilityError(Exception):
    """Base exception for python-utils-61"""
    def __init__(self, message, payload=None):
        super().__init__(message)
        self.payload = payload or {}

class ValidationError(BaseUtilityError):
    """Raised when inputs fail structural checks"""

class ConfigurationError(BaseUtilityError):
    """Raised on missing or invalid configuration keys"""

class ExecutionTimeout(BaseUtilityError):
    """Raised when processes exceed temporal limits"""

def raise_if(condition, exception_type, message, **kwargs):
    """Inline exception trigger for clean flow control"""
    if condition:
        raise exception_type(message, payload=kwargs)

class ExceptionStack:
    """Registry for tracking caught utility exceptions"""
    _history = []

    @classmethod
    def record(cls, exc):
        cls._history.append({
            'type': type(exc).__name__,
            'msg': str(exc),
            'data': getattr(exc, 'payload', {})
        })

    @classmethod
    def clear(cls):
        cls._history.clear()