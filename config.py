import os
import json
from typing import Any, Dict

class ConfigLoader:
    """Dynamic dictionary proxy with fallback logic."""
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "APP_"):
        self._store = defaults.copy()
        self._load_from_env(env_prefix)

    def _load_from_env(self, prefix: str) -> None:
        for key in self._store:
            env_key = f"{prefix}{key.upper()}"
            val = os.environ.get(env_key)
            if val:
                try:
                    self._store[key] = json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    self._store[key] = val

    def __getattr__(self, name: str) -> Any:
        if name in self._store:
            return self._store[name]
        raise AttributeError(f"Key {name} not found in configuration")

    def __getitem__(self, name: str) -> Any:
        return self._store[name]

    def update_from_file(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                self._store.update(data)

def create_config(defaults: Dict[str, Any]) -> ConfigLoader:
    return ConfigLoader(defaults)