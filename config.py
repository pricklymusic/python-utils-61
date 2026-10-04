import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "APP_"):
        self._data = defaults
        self._env_prefix = env_prefix

    def load_from_file(self, filepath: str) -> None:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self._data.update(json.load(f))
        self._apply_env_overrides()

    def _apply_env_overrides(self) -> None:
        for key in self._data:
            env_key = f"{self._env_prefix}{key.upper()}"
            if env_key in os.environ:
                val = os.environ[env_key]
                try:
                    self._data[key] = int(val)
                except ValueError:
                    self._data[key] = val

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __repr__(self) -> str:
        return f"Config({dict(self._data)})"