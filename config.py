import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._storage = defaults

    def __getitem__(self, key: str) -> Any:
        return self._storage.get(key)

    def load(self, path: str) -> None:
        try:
            with open(path, 'r') as f:
                user_data = json.load(f)
                self._storage.update(user_data)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def merge(self, overrides: Dict[str, Any]) -> None:
        self._storage.update(overrides)

    def __repr__(self) -> str:
        return f"<Config(keys={list(self._storage.keys())})>"

    def __getattr__(self, name: str) -> Any:
        return self._storage.get(name)

def create_config(defaults: Dict[str, Any]) -> ConfigLoader:
    return ConfigLoader(defaults)