import os
import json
from typing import Any, Dict

class ConfigLoader:
    """Dynamic dictionary proxy for configuration access."""
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "APP_"):
        self._data = defaults.copy()
        self._load_from_env(env_prefix)

    def _load_from_env(self, prefix: str) -> None:
        for key in self._data:
            env_val = os.getenv(f"{prefix}{key.upper()}")
            if env_val is not None:
                self._data[key] = self._cast(env_val)

    def _cast(self, val: str) -> Any:
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return val

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Config has no attribute {name}")

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __repr__(self) -> str:
        return f"ConfigLoader({dict(self._data)})"