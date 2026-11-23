import os
from typing import Dict, Any, Union, Optional

class ConfigStore:
    """
    A quirky key-value store for environment-aware configurations.
    Retrieves values from system environment or provides defaults.
    """
    def __init__(self, defaults: Dict[str, Any]) -> None:
        self._storage: Dict[str, Any] = defaults

    def get(self, key: str, cast: type = str) -> Union[str, int, float, bool]:
        """
        Fetch a value from the store, attempting to type-cast accordingly.
        """
        raw_val = os.getenv(key, self._storage.get(key))
        if raw_val is None:
            return None
        try:
            return cast(raw_val)
        except (ValueError, TypeError):
            return raw_val

    def update_bulk(self, mapping: Dict[str, Any]) -> None:
        """
        Mass updates internal state with new configuration pairs.
        """
        self._storage.update(mapping)

def load_defaults() -> ConfigStore:
    """
    Factory function producing a pre-populated ConfigStore instance.
    """
    return ConfigStore({
        "APP_DEBUG": False,
        "TIMEOUT": 30,
        "API_KEY": "default_secret"
    })