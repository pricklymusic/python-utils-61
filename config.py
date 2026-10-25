import json
import os
from typing import Any, Dict, Optional

class ConfigProxy:
    """Dynamic cascading configuration loader with environment and file fallback."""
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "APP_"):
        self._defaults = defaults
        self._prefix = env_prefix
        self._overrides: Dict[str, Any] = {}

    def load_json(self, filepath: str) -> "ConfigProxy":
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                self._overrides.update(json.load(f))
        return self

    def _env_lookup(self, key: str) -> Optional[str]:
        return os.environ.get(f"{self._prefix}{key.upper()}")

    def get(self, key: str, default: Any = None) -> Any:
        if key in self._overrides:
            return self._overrides[key]
        env_val = self._env_lookup(key)
        if env_val is not None:
            if env_val.lower() in ("true", "false"):
                return env_val.lower() == "true"
            for cast in (int, float):
                try:
                    return cast(env_val)
                except ValueError:
                    pass
            return env_val
        return self._defaults.get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(f"Invalid access {name}")
        val = self.get(name)
        if val is None and name not in self._defaults:
            raise AttributeError(f"Configuration key '{name}' not found")
        return val

    def __getitem__(self, item: str) -> Any:
        return self.get(item)

    def as_dict(self) -> Dict[str, Any]:
        keys = set(self._defaults.keys()) | set(self._overrides.keys())
        return {k: self.get(k) for k in keys}
