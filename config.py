import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "APP_"):
        self._data = defaults.copy()
        self._prefix = env_prefix

    def load_from_json(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, "r") as f:
                self._data.update(json.load(f))

    def __getattr__(self, name: str) -> Any:
        env_val = os.environ.get(f"{self._prefix}{name.upper()}")
        if env_val is not None:
            return self._cast(env_val)
        return self._data.get(name)

    def _cast(self, val: str) -> Any:
        if val.lower() in ("true", "yes"): return True
        if val.lower() in ("false", "no"): return False
        try:
            return int(val) if val.isdigit() else float(val)
        except ValueError:
            return val

    def __getitem__(self, key: str) -> Any:
        return self.__getattr__(key)

    def keys(self):
        return self._data.keys()