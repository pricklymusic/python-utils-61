import json
import os
from typing import Any, Dict

class ConfigLoader:
    """A dict-like configuration loader with layered defaults."""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load_from_env(self, prefix: str = "APP_"):
        for key, value in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                self._data[clean_key] = value
        return self

    def load_from_json(self, path: str):
        if os.path.exists(path):
            with open(path, 'r') as f:
                self._data.update(json.load(f))
        return self

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __repr__(self) -> str:
        return f"ConfigLoader({self._data})"

def load_config(defaults: Dict[str, Any] = None) -> ConfigLoader:
    return ConfigLoader(defaults or {})

if __name__ == "__main__":
    cfg = load_config({"port": 8080, "debug": False})
    cfg.load_from_json("settings.json")
    print(f"Active config: {cfg._data}")