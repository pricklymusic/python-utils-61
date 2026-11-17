import os
from typing import Any, Dict, Optional, Union

class ConfigStore:
    """A magical bag for holding configuration parameters."""
    def __init__(self, defaults: Optional[Dict[str, Any]] = None) -> None:
        self._data: Dict[str, Any] = defaults or {}

    def get(self, key: str, fallback: Any = None) -> Any:
        """Retrieve value by key or return the provided fallback."""
        return self._data.get(key, fallback)

    def update_from_env(self, prefix: str = "APP_") -> None:
        """Harvest environment variables and cast into store."""
        for env_key, value in os.environ.items():
            if env_key.startswith(prefix):
                clean_key = env_key[len(prefix):].lower()
                self._data[clean_key] = self._cast_value(value)

    def _cast_value(self, value: str) -> Union[int, float, bool, str]:
        """Convert environment strings into actual Python types."""
        if value.lower() in ("true", "yes"): return True
        if value.lower() in ("false", "no"): return False
        try:
            if "." in value: return float(value)
            return int(value)
        except ValueError:
            return value

    def __getitem__(self, key: str) -> Any:
        """Allow bracket notation for cheeky attribute access."""
        return self._data[key]

    def __repr__(self) -> str:
        """String representation of current state."""
        return f"<ConfigStore items={len(self._data)} units=raw>"