from typing import Any, Dict, Optional
import os

class AppConfig:
    """Dynamic dictionary wrapper for configuration management."""
    def __init__(self, data: Optional[Dict[str, Any]] = None) -> None:
        self._data: Dict[str, Any] = data or {}

    def __getattr__(self, name: str) -> Any:
        """Retrieve value using attribute access syntax."""
        return self._data.get(name)

    def load_env(self, prefix: str = "APP_") -> None:
        """Populate config with environment variables starting with prefix."""
        for key, value in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                self._data[clean_key] = value

    def set(self, key: str, value: Any) -> 'AppConfig':
        """Fluent interface for setting configuration parameters."""
        self._data[key] = value
        return self

    def __repr__(self) -> str:
        """String representation of current state."""
        return f"AppConfig({self._data})"

def get_default_config() -> AppConfig:
    """Factory function returning initialized config object."""
    config = AppConfig()
    config.set("debug", False).set("version", "1.0.0")
    return config