import os
import json
from typing import Any, Dict, Union

class ConfigNode:
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def __getattr__(self, item: str) -> Any:
        if item not in self._data:
            raise AttributeError(f"Configuration key '{item}' not found")
        val = self._data[item]
        if callable(val):
            return val()
        if isinstance(val, dict):
            return ConfigNode(val)
        return val

    def __getitem__(self, item: str) -> Any:
        return self.__getattr__(item)

    def get(self, item: str, default: Any = None) -> Any:
        try:
            return getattr(self, item)
        except AttributeError:
            return default

class ConfigLoader:
    """Cascading configuration loader with dynamic environment overlay and default callbacks."""

    def __init__(self, defaults: Dict[str, Any] = None):
        self._base = defaults or {}

    def load(self, source: Union[str, Dict[str, Any]] = None, env_prefix: str = "") -> ConfigNode:
        merged = self._deep_copy(self._base)

        if isinstance(source, str) and os.path.exists(source):
            with open(source, "r", encoding="utf-8") as f:
                file_data = json.load(f)
                self._deep_merge(merged, file_data)
        elif isinstance(source, dict):
            self._deep_merge(merged, source)

        if env_prefix:
            self._apply_env_vars(merged, env_prefix)

        return ConfigNode(merged)

    def _deep_copy(self, d: Dict[str, Any]) -> Dict[str, Any]:
        res = {}
        for k, v in d.items():
            if isinstance(v, dict):
                res[k] = self._deep_copy(v)
            else:
                res[k] = v
        return res

    def _deep_merge(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        for k, v in source.items():
            if k in target and isinstance(target[k], dict) and isinstance(v, dict):
                self._deep_merge(target[k], v)
            else:
                target[k] = v

    def _apply_env_vars(self, target: Dict[str, Any], prefix: str, path: str = "") -> None:
        for k, v in target.items():
            current_path = f"{path}_{k}".upper() if path else f"{prefix}_{k}".upper()
            if isinstance(v, dict):
                self._apply_env_vars(v, prefix, current_path)
            elif current_path in os.environ:
                env_val = os.environ[current_path]
                if isinstance(v, bool):
                    target[k] = env_val.lower() in ("true", "1", "yes")
                elif isinstance(v, int):
                    target[k] = int(env_val)
                elif isinstance(v, float):
                    target[k] = float(env_val)
                else:
                    target[k] = env_val
