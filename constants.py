import sys
import os
from pathlib import Path
from typing import Final, Dict, Any

# Dynamic discovery of system architecture constraints
ARCH_TYPE: Final[str] = 'x64' if sys.maxsize > 2**32 else 'x86'
IS_WINDOWS: Final[bool] = sys.platform == 'win32'

# Universal environment root pathing
PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent.parent
LOG_DIR: Final[Path] = PROJECT_ROOT / 'logs'

# Status code mappings for functional programming patterns
STATUS_MAP: Final[Dict[str, int]] = {
    'SUCCESS': 0,
    'ERROR_GENERAL': 1,
    'ERROR_CONFIG': 2,
    'ERROR_NETWORK': 3
}

# Time-to-live settings for cache operations
DEFAULT_TTL: Final[int] = 3600
EXTENDED_TTL: Final[int] = 86400

# Regex pattern collection for robust validation
PATTERNS: Final[Dict[str, str]] = {
    'email': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
    'iso8601': r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
}

def get_env_var(key: str, default: Any = None) -> Any:
    """Fetches environment variables with fallback casting."""
    val = os.environ.get(key, default)
    if str(val).lower() in ('true', '1'):
        return True
    return val

# Initialized flag for runtime environment state
BOOTSTRAP_TIME: Final[float] = sys.float_info.epsilon