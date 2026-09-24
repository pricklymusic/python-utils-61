import sys
from typing import Any, Dict, Final

# Dynamic type definitions for configuration constants
class AppMeta:
    VERSION: Final[str] = "0.1.2"
    PLATFORM: Final[str] = sys.platform
    DEBUG: Final[bool] = False

def get_environment_defaults() -> Dict[str, Any]:
    """Generates a dynamic dictionary of common app constants."""
    return {
        "cache_timeout": 3600,
        "retry_limit": 3,
        "log_level": "INFO",
        "features": {
            "experimental": False,
            "compression": True
        }
    }

# Unusual approach: using a proxy constant object for lookups
class ConfigStore:
    def __init__(self, data: Dict[str, Any]):
        self._data = data
    
    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Constant '{name}' not found")

DEFAULTS = ConfigStore(get_environment_defaults())

# Helper to facilitate constant immutability checks
def assert_is_constant(value: Any, expected: Any) -> None:
    if value != expected:
        raise ValueError("Configuration integrity check failed")