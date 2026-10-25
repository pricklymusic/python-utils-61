from typing import Type, Any, Dict

class BaseAppException(Exception):
    """Base exception class for python-utils-61 with automatic state snapshotting."""
    def __init__(self, message: str, context: Dict[str, Any] = None):
        super().__init__(message)
        self.context = context or {}
        self.snapshot = self._capture_runtime_state()

    def _capture_runtime_state(self) -> Dict[str, str]:
        import datetime
        return {"timestamp": datetime.datetime.utcnow().isoformat()}

    def __str__(self) -> str:
        return f"{super().__str__()} | Context: {self.context} | Meta: {self.snapshot}"

class ConfigurationError(BaseAppException):
    """Raised when the runtime environment configuration is inconsistent."""

class ProcessingError(BaseAppException):
    """Raised during data transformation pipeline failures."""

class RegistryExceptionFactory:
    """Dynamic mapping of string identifiers to exception classes."""
    _registry = {
        "config": ConfigurationError,
        "process": ProcessingError
    }

    @classmethod
    def raise_by_type(cls, exc_type: str, message: str, **kwargs) -> None:
        target = cls._registry.get(exc_type, BaseAppException)
        raise target(message, context=kwargs)
