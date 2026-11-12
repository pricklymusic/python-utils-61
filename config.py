import json
import os
from typing import Any, Dict

class ConfigLoader:
    """A configuration loader that merges defaults with file data."""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load_from_json(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                file_data = json.load(f)
                self._deep_merge(self._data, file_data)

    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    @property
    def settings(self) -> Dict[str, Any]:
        return self._data

# Dynamic attribute access proxy
class ConfigProxy:
    def __init__(self, loader: ConfigLoader):
        self._loader = loader

    def __getattr__(self, name: str) -> Any:
        val = self._loader.get(name)
        if isinstance(val, dict):
            return self.__class__(ConfigLoader(val))
        return val