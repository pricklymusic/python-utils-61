import json
import os
from typing import Any, Dict, Optional


class ConfigStore:
    """Dynamic configuration loader with default cascading and env overrides."""

    def __init__(self, defaults: Optional[Dict[str, Any]] = None, env_prefix: str = "APP_") -> None:
        self._defaults = defaults or {}
        self._env_prefix = env_prefix
        self._user_config: Dict[str, Any] = {}

    def load_from_file(self, path: str) -> "ConfigStore":
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self._user_config.update(json.load(f))
        return self

    def load_from_dict(self, data: Dict[str, Any]) -> "ConfigStore":
        self._user_config.update(data)
        return self

    def _cast_type(self, raw_val: str, target_type: type) -> Any:
        if target_type is bool:
            return raw_val.lower() in ("true", "1", "yes", "on")
        try:
            return target_type(raw_val)
        except (ValueError, TypeError):
            return raw_val

    def get(self, key: str, default: Any = None) -> Any:
        env_key = f"{self._env_prefix}{key.upper().replace('.', '_')}"
        if env_key in os.environ:
            env_val = os.environ[env_key]
            ref_val = self._resolve_path(self._user_config, key) or self._resolve_path(self._defaults, key) or default
            return self._cast_type(env_val, type(ref_val)) if ref_val is not None else env_val

        user_val = self._resolve_path(self._user_config, key)
        if user_val is not None:
            return user_val

        def_val = self._resolve_path(self._defaults, key)
        if def_val is not None:
            return def_val

        return default

    def _resolve_path(self, source: Dict[str, Any], path: str) -> Any:
        curr = source
        for step in path.split("."):
            if isinstance(curr, dict) and step in curr:
                curr = curr[step]
            else:
                return None
        return curr

    def __getitem__(self, item: str) -> Any:
        val = self.get(item)
        if val is None:
            raise KeyError(f"Configuration key '{item}' not found")
        return val

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        return self.get(name)
