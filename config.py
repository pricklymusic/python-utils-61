import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults.copy()

    def load_from_env(self, prefix: str = 'APP_'):
        for key, value in self._data.items():
            env_key = f"{prefix}{key.upper()}"
            if env_key in os.environ:
                raw = os.environ[env_key]
                try:
                    self._data[key] = json.loads(raw)
                except json.JSONDecodeError:
                    self._data[key] = raw
        return self

    def load_from_file(self, path: str):
        if os.path.exists(path):
            with open(path, 'r') as f:
                self._data.update(json.load(f))
        return self

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def __repr__(self) -> str:
        return f"Config({self._data})"