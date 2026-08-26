import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "APP_") -> None:
        self._config = dict(defaults)
        self._env_prefix = env_prefix
        self._load_env()

    def _load_env(self) -> None:
        for key in self._config:
            env_name = f"{self._env_prefix}{key.upper()}"
            if env_name in os.environ:
                val = os.environ[env_name]
                self._config[key] = self._cast(val, type(self._config[key]))

    @staticmethod
    def _cast(val: str, target_type: type) -> Any:
        if target_type is bool:
            return val.lower() in ("true", "1", "yes", "on")
        try:
            return target_type(val)
        except (ValueError, TypeError):
            return val

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._config[key]

    def __contains__(self, key: str) -> bool:
        return key in self._config

def load_config(defaults: Dict[str, Any], prefix: str = "APP_") -> ConfigLoader:
    return ConfigLoader(defaults, env_prefix=prefix)
