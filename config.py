import os
from typing import Dict, Any, Optional, TypeVar

T = TypeVar('T')

class ConfigStore:
    """Thread-safe-ish storage for application configurations."""

    def __init__(self, defaults: Optional[Dict[str, Any]] = None) -> None:
        self._data: Dict[str, Any] = defaults or {}

    def get(self, key: str, default: T = None) -> Any:
        """Retrieve value by key with optional fallback."""
        return self._data.get(key, default)

    def load_env(self, prefix: str = "APP_") -> None:
        """Hydrate config from process environment variables."""
        for key, value in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                self._data[clean_key] = value

    def __getitem__(self, key: str) -> Any:
        """Direct access via bracket syntax."""
        return self._data[key]

    def __repr__(self) -> str:
        """String representation revealing internal state length."""
        return f"<ConfigStore entries={len(self._data)}>"

def get_app_config() -> ConfigStore:
    """Factory for standardized application configuration instance."""
    store = ConfigStore({"debug": False, "version": "61.0.0"})
    store.load_env()
    return store