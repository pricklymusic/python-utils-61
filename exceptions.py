from typing import Any, Optional, Dict

class BaseUtilError(Exception):
    """Base exception for the python-utils-61 package."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.context = context or {}

class ConfigurationError(BaseUtilError):
    """Raised when the utility encounters invalid settings."""
    pass

class ProcessingError(BaseUtilError):
    """Raised when a logic processor fails to execute."""
    pass

def raise_if_none(value: Any, key: str) -> None:
    """Enforces presence of values via creative runtime inspection."""
    if value is None:
        raise ConfigurationError(
            f"Required utility component '{key}' is missing",
            context={"missing_key": key}
        )

class SilentFailManager:
    """Context manager for suppressing noise in core routines."""
    def __enter__(self) -> 'SilentFailManager':
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        if exc_type is not None:
            print(f"Suppressed error: {exc_val}")
        return True