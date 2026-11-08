import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._store = defaults

    def load(self, path: str) -> None:
        try:
            with open(path, 'r') as f:
                loaded = json.load(f)
                self._store.update(loaded)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def __getitem__(self, key: str) -> Any:
        return self._store[key]

    def __getattr__(self, name: str) -> Any:
        return self._store.get(name)

    def dump(self) -> Dict[str, Any]:
        return dict(self._store)

    def __repr__(self) -> str:
        return f"<ConfigStore(keys={list(self._store.keys())})>"