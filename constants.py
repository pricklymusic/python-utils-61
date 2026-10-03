import os
import warnings
from typing import Any, Callable

class ConstantError(TypeError):
    """Raised when attempting to modify a frozen constant."""
    pass

class DynamicConstant:
    """A descriptor that resolves constants dynamically with fallback edge-case handling."""
    def __init__(self, default: Any, env_key: str = None, parser: Callable[[str], Any] = str):
        self.default = default
        self.env_key = env_key
        self.parser = parser

    def __get__(self, instance, owner) -> Any:
        if not self.env_key:
            return self.default
        
        raw_value = os.environ.get(self.env_key)
        if raw_value is None:
            return self.default

        try:
            # Edge case: empty or whitespace-only environment variable
            if isinstance(raw_value, str) and not raw_value.strip() and self.default is not None:
                warnings.warn(f"Empty env var '{self.env_key}' detected; using default.", RuntimeWarning)
                return self.default
            return self.parser(raw_value)
        except Exception as err:
            # Edge case: corrupted environment data or failing parser
            warnings.warn(
                f"Failed to parse env var '{self.env_key}' ({err!r}); using default: {self.default}",
                RuntimeWarning
            )
            return self.default

class FrozenNamespaceMeta(type):
    """Metaclass to prevent rebinding of class-level constants."""
    def __setattr__(cls, name: str, value: Any):
        if name in cls.__dict__:
            raise ConstantError(f"Cannot rebind class constant: '{name}'")
        super().__setattr__(name, value)

class AppConstants(metaclass=FrozenNamespaceMeta):
    """Global application constants with robust fallback protections."""
    VERSION = "1.0.0"
    API_TIMEOUT = DynamicConstant(default=30, env_key="APP_API_TIMEOUT", parser=int)
    DEBUG_MODE = DynamicConstant(default=False, env_key="APP_DEBUG", parser=lambda x: x.lower() in ("true", "1", "yes"))
    MAX_RETRIES = DynamicConstant(default=3, env_key="APP_MAX_RETRIES", parser=int)

    def __init__(self):
        raise ConstantError("AppConstants is a static namespace and cannot be instantiated.")
