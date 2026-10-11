import sys
from typing import Any, Dict, Optional, Type


class MetaUtilError(type):
    """Metaclass that automatically catalogs exception types by code."""

    _registry: Dict[str, Type["BaseUtilError"]] = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if name != "BaseUtilError":
            code = getattr(cls, "code", name.lower().replace("error", ""))
            cls._registry[code] = cls


class BaseUtilError(Exception, metaclass=MetaUtilError):
    """Base exception supporting fluent context chaining and structural reporting."""

    code: str = "generic"

    def __init__(self, message: str, payload: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.payload = payload or {}

    def attach(self, **kwargs: Any) -> "BaseUtilError":
        """Attach runtime context key-values in a chainable manner."""
        self.payload.update(kwargs)
        return self

    def format_details(self) -> str:
        """Render error message with formatted context metadata."""
        lines = [f"[{self.code.upper()}] {self.message}"]
        if self.payload:
            lines.extend(f"  > {k} = {v!r}" for k, v in self.payload.items())
        return "\n".join(lines)


class ValidationError(BaseUtilError):
    code = "validation_failure"


class ProcessingError(BaseUtilError):
    code = "processing_failure"


class ConfigurationError(BaseUtilError):
    code = "configuration_invalid"


def resolve_error_class(code: str) -> Type[BaseUtilError]:
    """Resolve error class dynamically from registered codes."""
    return MetaUtilError._registry.get(code, BaseUtilError)
