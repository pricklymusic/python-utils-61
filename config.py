import json
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], config_path: str = "config.json"):
        self._data = defaults.copy()
        self._path = Path(config_path)
        self._load_file()

    def _load_file(self) -> None:
        if self._path.exists():
            try:
                with open(self._path, "r") as f:
                    self._data.update(json.load(f))
            except (json.JSONDecodeError, IOError):
                pass

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Config key '{name}' missing")

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def save(self) -> None:
        with open(self._path, "w") as f:
            json.dump(self._data, f, indent=4)

    def merge(self, overrides: Dict[str, Any]) -> None:
        self._data.update(overrides)

def get_config(defaults: Dict[str, Any]) -> ConfigLoader:
    return ConfigLoader(defaults)