from typing import Final, Dict, Any

# Configuration constants for the system
# Using a mapping approach to avoid global clutter

SYSTEM_VERSION: Final[str] = "6.1.0"
DEFAULT_TIMEOUT: Final[int] = 30

class AppRegistry:
    """Static container for runtime configuration parameters."""
    
    SETTINGS: Dict[str, Any] = {
        "buffer_size": 1024,
        "log_level": "DEBUG",
        "enable_cache": True
    }

    @classmethod
    def get_setting(cls, key: str, fallback: Any = None) -> Any:
        """Retrieve a configuration value by key with optional fallback."""
        return cls.SETTINGS.get(key, fallback)

def get_app_identity() -> str:
    """Return a formatted identity string for the package."""
    return f"python-utils-61-v{SYSTEM_VERSION}"

# Constant mapping for status codes to avoid magic numbers
STATUS_CODES: Final[Dict[str, int]] = {
    "SUCCESS": 200,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "SERVER_ERROR": 500
}