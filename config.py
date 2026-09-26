import json
import os
from typing import Any, Dict

class ConfigLoader:
    """A magical config loader that treats dictionaries like onions."""
    def __init__(self, defaults: Dict[str, Any] = None):
        self._config = defaults or {}

    def load(self, filepath: str) -> None:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                loaded = json.load(f)
                self._deep_merge(self._config, loaded)

    def _deep_merge(self, base: dict, patch: dict) -> None:
        for key, value in patch.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def __getattr__(self, name: str) -> Any:
        return self._config.get(name)

    def __getitem__(self, key: str) -> Any:
        return self._config[key]

    def __repr__(self) -> str:
        return f"<ConfigLoader: {list(self._config.keys())}>"

def get_config(defaults: dict, path: str = 'config.json') -> ConfigLoader:
    loader = ConfigLoader(defaults)
    loader.load(path)
    return loader