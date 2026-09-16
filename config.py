import json
import os
from typing import Any, Dict


class ConfigLoader:
    """A dynamic configuration loader supporting defaults, environment overrides, and attribute-style access."""

    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "APP_"):
        self.__dict__["_defaults"] = defaults
        self.__dict__["_prefix"] = env_prefix
        self.__dict__["_data"] = {}

    def load_from_json(self, filepath: str) -> None:
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                self.__dict__["_data"].update(json.load(f))

    def __getattr__(self, name: str) -> Any:
        env_key = f"{self._prefix}{name.upper()}"
        if env_key in os.environ:
            val = os.environ[env_key]
            default_val = self._defaults.get(name)
            if default_val is not None:
                try:
                    return type(default_val)(val)
                except (ValueError, TypeError):
                    return val
            return val

        if name in self._data:
            return self._data[name]

        if name in self._defaults:
            return self._defaults[name]

        raise AttributeError(f"Configuration key '{name}' is not defined")

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("Configuration is read-only")

    def get_all(self) -> Dict[str, Any]:
        all_keys = (
            set(self._defaults.keys())
            | set(self._data.keys())
            | {
                k[len(self._prefix) :].lower()
                for k in os.environ
                if k.startswith(self._prefix)
            }
        )
        return {k: getattr(self, k) for k in sorted(all_keys) if k}
