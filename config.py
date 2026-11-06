import os
import json
from typing import Any, Dict, Union

class ConfigProxy:
    """Dynamic configuration cascade supporting attribute access, env variables, and callable defaults."""
    def __init__(self, data: Dict[str, Any] = None, defaults: Dict[str, Any] = None, env_prefix: str = "APP_"):
        self._data = data or {}
        self._defaults = defaults or {}
        self._prefix = env_prefix

    def _resolve_env(self, key: str) -> Union[str, None]:
        env_key = f"{self._prefix}{key.upper()}"
        return os.environ.get(env_key)

    def get(self, key: str, fallback: Any = None) -> Any:
        if key in self._data:
            val = self._data[key]
        elif (env_val := self._resolve_env(key)) is not None:
            val = env_val
        elif key in self._defaults:
            val = self._defaults[key]
        else:
            val = fallback

        if callable(val):
            val = val()

        if isinstance(val, dict):
            sub_defaults = self._defaults.get(key, {}) if isinstance(self._defaults.get(key), dict) else {}
            return ConfigProxy(val, sub_defaults, f"{self._prefix}{key.upper()}_")

        return val

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        return self.get(name)

    def __getitem__(self, item: str) -> Any:
        return self.get(item)

    def to_dict(self) -> Dict[str, Any]:
        keys = set(self._data.keys()) | set(self._defaults.keys())
        res = {}
        for k in keys:
            v = self.get(k)
            res[k] = v.to_dict() if isinstance(v, ConfigProxy) else v
        return res

    @classmethod
    def load_json(cls, path: str, defaults: Dict[str, Any] = None) -> "ConfigProxy":
        content = {}
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = json.load(f)
        return cls(content, defaults)
