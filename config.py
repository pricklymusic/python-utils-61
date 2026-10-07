import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def load_json(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                file_data = json.load(f)
                self._data.update(file_data)

    def __getattr__(self, key: str) -> Any:
        return self._data.get(key)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def items(self):
        return self._data.items()

    def inject_env(self, prefix: str = "APP_"):
        for key, value in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                self._data[clean_key] = value

    def __repr__(self):
        return f"Config(keys={list(self._data.keys())})"