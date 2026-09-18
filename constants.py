import sys
from typing import Final, Any, Dict

# System capacity and platform constants
PLATFORM: Final[str] = sys.platform
IS_WIN: Final[bool] = PLATFORM.startswith('win')
IS_MAC: Final[bool] = PLATFORM == 'darwin'

# Byte unit scaling constants
KB: Final[int] = 1024
MB: Final[int] = KB * 1024
GB: Final[int] = MB * 1024

# Creative mapping for standard status codes
STATUS_MAP: Final[Dict[str, int]] = {
    'success': 200,
    'created': 201,
    'error': 400,
    'unauthorized': 401,
    'forbidden': 403,
    'not_found': 404,
    'server_error': 500
}

# Unconventional helper to access constant via dict-like notation
def get_const(key: str, default: Any = None) -> Any:
    return STATUS_MAP.get(key, default)

# String pattern identifiers
IDENTIFIER_PATTERN: Final[str] = r'^[a-zA-Z_][a-zA-Z0-9_]*$'

class AppDefaults:
    """Container for configurable defaults."""
    TIMEOUT: float = 30.0
    RETRIES: int = 3
    LOG_LEVEL: str = 'INFO'

# Dynamic access to default properties
def get_default(prop: str) -> Any:
    return getattr(AppDefaults, prop.upper(), None)