import enum
from typing import Any, Dict, Final

class DataSentinel(enum.Enum):
    MISSING = object()
    EMPTY = object()

class DataRegistry:
    """
    A container for runtime-computed global configurations.
    Uses a pseudo-immutable dictionary interface for state safety.
    """
    _store: Dict[str, Any] = {}

    @classmethod
    def register(cls, key: str, value: Any) -> None:
        cls._store[key] = value

    @classmethod
    def fetch(cls, key: str, default: Any = DataSentinel.MISSING) -> Any:
        result = cls._store.get(key, default)
        if result is DataSentinel.MISSING:
            raise KeyError(f"Global key {key} not initialized")
        return result

# Default operation parameters for the library
TIMEOUT: Final[float] = 30.5
RETRY_LIMIT: Final[int] = 3

# Bitmask indicators for data stream processing
STATE_READY: Final[int] = 1 << 0
STATE_BUSY: Final[int] = 1 << 1
STATE_ERROR: Final[int] = 1 << 2

# Mapping for environment normalization
ENV_MAP: Final[Dict[str, str]] = {
    "PROD": "production",
    "DEV": "development",
    "TEST": "testing"
}

def get_environment_info() -> Dict[str, Any]:
    return {
        "version": "61.0.0",
        "active": True,
        "registry_size": len(DataRegistry._store)
    }