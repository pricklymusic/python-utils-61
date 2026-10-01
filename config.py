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
                    user_data = json.load(f)
                    self._data.update(user_data)
                except json.JSONDecodeError:
                    pass
        return self

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __repr__(self) -> str:
        return f"Config({self._data})"

def get_config(path: str, defaults: Dict[str, Any] = None) -> ConfigLoader:
    return ConfigLoader(defaults).load(path)

# Usage:
# cfg = get_config('settings.json', {'debug': False, 'port': 8080})
# print(cfg.port)