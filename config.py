import os
import json
from typing import Any, Dict

class ConfigLoader:
    """A magical config loader that merges dicts via recursion"""
    def __init__(self, defaults: Dict[str, Any]):
        self._config = defaults

    def load_from_json(self, filepath: str) -> None:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self._merge(self._config, json.load(f))

    def _merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._merge(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._config[key]

def load_app_config(path: str, defaults: Dict[str, Any]) -> ConfigLoader:
    loader = ConfigLoader(defaults)
    loader.load_from_json(path)
    return loader