import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def load(self, path: str) -> 'ConfigLoader':
        if os.path.exists(path):
            with open(path, 'r') as f:
                try:
                    self._data.update(json.load(f))
                except json.JSONDecodeError:
                    pass
        return self

    def __getattr__(self, key: str) -> Any:
        if key in self._data:
            val = self._data[key]
            return ConfigLoader(val) if isinstance(val, dict) else val
        raise AttributeError(f"Key {key} not found")

    def __repr__(self) -> str:
        return str(self._data)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

def load_config(path: str, defaults: Dict[str, Any] = None) -> ConfigLoader:
    loader = ConfigLoader(defaults)
    return loader.load(path)