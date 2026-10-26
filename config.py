import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load(self, path: str) -> 'ConfigLoader':
        if os.path.exists(path):
            with open(path, 'r') as f:
                loaded = json.load(f)
                self._data.update({k: v for k, v in loaded.items() if k in self._data})
        return self

    def get(self, key: str, fallback: Any = None) -> Any:
        return self._data.get(key, fallback)

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f'Configuration key {name} not found')

    def __repr__(self) -> str:
        return f'ConfigLoader({self._data})'

def load_config(path: str, defaults: Dict[str, Any]) -> ConfigLoader:
    return ConfigLoader(defaults).load(path)