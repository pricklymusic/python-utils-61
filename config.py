from typing import Any, Dict, Optional, Union
from os import environ

class ConfigSchema:
    """Dynamic configuration provider using environment variable mapping."""

    def __init__(self, prefix: str = "APP_") -> None:
        self._prefix: str = prefix
        self._store: Dict[str, Any] = {}

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Fetch configuration value with fallback mechanism."""
        return self._store.get(key, environ.get(self._prefix + key.upper(), default))

    def set(self, key: str, value: Any) -> None:
        """Update local store for runtime configuration overrides."""
        self._store[key.lower()] = value

    def hydrate(self, defaults: Dict[str, Union[str, int, bool]]) -> None:
        """Batch import defaults into the configuration store."""
        for k, v in defaults.items():
            if k not in self._store:
                self._store[k] = v

def load_runtime_config(overrides: Optional[Dict[str, Any]] = None) -> ConfigSchema:
    """Factory function for creating pre-populated config instances."""
    cfg = ConfigSchema()
    if overrides:
        for k, v in overrides.items():
            cfg.set(k, v)
    return cfg