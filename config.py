import os
import json
from collections import ChainMap
from typing import Any, Dict, Optional

class ConfigLoader:
    """Hierarchical configuration manager with dynamic attributes and env overrides."""

    def __init__(self, defaults: Optional[Dict[str, Any]] = None, env_prefix: str = "APP_"):
        self._defaults = defaults or {}
        self._loaded: Dict[str, Any] = {}
        self._env_prefix = env_prefix

    def load_file(self, path: str) -> "ConfigLoader":
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                self._loaded.update(json.load(file))
        return self

    def override(self, **kwargs: Any) -> "ConfigLoader":
        self._loaded.update(kwargs)
        return self

    def _resolve(self, key: str) -> Any:
        env_var = f"{self._env_prefix}{key.upper()}"
        if env_var in os.environ:
            raw = os.environ[env_var]
            return json.loads(raw) if raw.startswith(("{", "[", '"')) else raw
        
        sources = ChainMap(self._loaded, self._defaults)
        if key in sources:
            return sources[key]
        raise KeyError(f"Configuration key '{key}' is undefined")

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self._resolve(key)
        except KeyError:
            return default

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            return super().__getattribute__(name)
        try:
            return self._resolve(name)
        except KeyError as err:
            raise AttributeError(str(err)) from err

    def __getitem__(self, item: str) -> Any:
        return self._resolve(item)

    def as_dict(self) -> Dict[str, Any]:
        return {**self._defaults, **self._loaded}
