import os
from typing import Any, Dict

class ConfigLoader(dict):
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "APP_") -> None:
        super().__init__(defaults)
        self.env_prefix = env_prefix
        self._load_from_env()

    def __getattr__(self, key: str) -> Any:
        try:
            return self[key]
        except KeyError as err:
            raise AttributeError(f"Configuration key not found: {err}")

    def __setattr__(self, key: str, value: Any) -> None:
        self[key] = value

    def _load_from_env(self) -> None:
        for key in self.keys():
            env_name = f"{self.env_prefix}{key.upper()}"
            if env_name in os.environ:
                val = os.environ[env_name]
                self[key] = self._coerce(self[key], val)

    @staticmethod
    def _coerce(original: Any, val: str) -> Any:
        if isinstance(original, bool):
            return val.lower() in ("true", "1", "yes", "on")
        if isinstance(original, int):
            return int(val)
        if isinstance(original, float):
            return float(val)
        return val

    def update_with_file(self, filepath: str) -> None:
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                for line in f:
                    if "=" in line and not line.strip().startswith("#"):
                        k, v = line.strip().split("=", 1)
                        k, v = k.strip().lower(), v.strip()
                        if k in self:
                            self[k] = self._coerce(self[k], v)
