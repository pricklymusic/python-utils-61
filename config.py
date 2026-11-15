import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "APP_"):
        self._data = defaults.copy()
        self._env_prefix = env_prefix
        self._load_from_env()

    def _load_from_env(self) -> None:
        for key in self._data:
            env_key = f"{self._env_prefix}{key.upper()}"
            if env_key in os.environ:
                raw_val = os.environ[env_key]
                try:
                    self._data[key] = json.loads(raw_val)
                except (json.JSONDecodeError, TypeError):
                    self._data[key] = raw_val

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def get(self, key: str, fallback: Any = None) -> Any:
        return self._data.get(key, fallback)

    def __repr__(self) -> str:
        return f"ConfigLoader({self._data})"

def load_config(defaults: Dict[str, Any]) -> ConfigLoader:
    return ConfigLoader(defaults)