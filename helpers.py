import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic configuration loader with recursive default merging."""
    def __init__(self, defaults: Dict[str, Any] = None):
        self._config = defaults or {}

    def load(self, path: str) -> 'ConfigLoader':
        if os.path.exists(path):
            with open(path, 'r') as f:
                file_data = json.load(f)
                self._deep_merge(self._config, file_data)
        return self

    def _deep_merge(self, base: Dict, update: Dict) -> None:
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def __getattr__(self, name: str) -> Any:
        return self._config.get(name)

def load_config(path: str, defaults: Dict = None) -> ConfigLoader:
    loader = ConfigLoader(defaults)
    return loader.load(path)