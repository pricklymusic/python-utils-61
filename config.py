import os
from typing import Any, Dict

class ConfigRegistry:
    """Dynamic configuration container with dictionary-like access."""
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def load_env(self, prefix: str = "APP_") -> None:
        for key, value in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                self._data[clean_key] = value

    def update(self, mapping: Dict[str, Any]) -> None:
        self._data.update(mapping)

    def __repr__(self) -> str:
        return f"ConfigRegistry({list(self._data.keys())})"

def get_app_config() -> ConfigRegistry:
    config = ConfigRegistry({
        "debug": False,
        "version": "1.0.0",
        "timeout": 30
    })
    config.load_env()
    return config

settings = get_app_config()