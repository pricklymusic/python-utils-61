import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic configuration loader with fallback defaults."""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults.copy()

    def load_from_env(self, prefix: str = 'APP_'):
        """Override defaults with environment variables."""
        for key in self._data:
            env_key = f"{prefix}{key.upper()}"
            if env_key in os.environ:
                self._data[key] = os.environ[env_key]
        return self

    def load_from_json(self, path: str):
        """Merge JSON file into configuration."""
        if os.path.exists(path):
            with open(path, 'r') as f:
                self._data.update(json.load(f))
        return self

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def __repr__(self) -> str:
        return f"Config({self._data})"

# Usage example:
# config = ConfigLoader({'port': 8080, 'debug': False})
# config.load_from_json('cfg.json').load_from_env()
# print(config.port)