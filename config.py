import json
import os
from pathlib import Path
from typing import Any, Dict, Union


class DynamicConfig:
    """Configuration loader with dynamic attribute access, defaults, and env overrides."""

    def __init__(
        self,
        defaults: Dict[str, Any] = None,
        env_prefix: str = "APP_",
    ):
        self._defaults = defaults or {}
        self._env_prefix = env_prefix
        self._data: Dict[str, Any] = {}

    def load_from_dict(self, data: Dict[str, Any]) -> "DynamicConfig":
        self._data.update(data)
        return self

    def load_from_file(self, path: Union[str, Path]) -> "DynamicConfig":
        path = Path(path)
        if path.exists() and path.suffix == ".json":
            with path.open("r", encoding="utf-8") as f:
                self._data.update(json.load(f))
        return self

    def _resolve_env(self, key_path: str) -> Any:
        env_var = f"{self._env_prefix}{key_path.upper().replace('.', '__')}"
        return os.getenv(env_var)

    def get(self, key: str, fallback: Any = None) -> Any:
        env_val = self._resolve_env(key)
        if env_val is not None:
            return env_val

        keys = key.split(".")
        curr_data = self._data
        curr_default = self._defaults

        for k in keys:
            if isinstance(curr_data, dict) and k in curr_data:
                curr_data = curr_data[k]
            else:
                curr_data = None
                break

        if curr_data is not None:
            return curr_data

        for k in keys:
            if isinstance(curr_default, dict) and k in curr_default:
                curr_default = curr_default[k]
            else:
                return fallback

        return curr_default

    def __getattr__(self, name: str) -> Any:
        val = self.get(name)
        if val is None:
            raise AttributeError(f"Configuration key '{name}' not found")
        if isinstance(val, dict):
            return DynamicConfig(defaults=val, env_prefix=self._env_prefix)
        return val
