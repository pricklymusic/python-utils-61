import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._config = defaults or {}

    def __getattr__(self, name: str) -> Any:
        return self._config.get(name)

    def load_from_json(self, filepath: str) -> None:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self._config.update(json.load(f))

    def load_from_env(self, prefix: str = 'APP_') -> None:
        for key, value in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                self._config[clean_key] = self._parse_env_value(value)

    def _parse_env_value(self, val: str) -> Any:
        if val.lower() in ('true', 'yes'): return True
        if val.lower() in ('false', 'no'): return False
        try:
            return int(val) if val.isdigit() else float(val)
        except ValueError:
            return val

def get_config(defaults: Dict[str, Any] = None) -> ConfigLoader:
    return ConfigLoader(defaults or {})

if __name__ == '__main__':
    cfg = get_config({'port': 8080, 'host': 'localhost'})
    cfg.load_from_env()
    print(f'Active config: {cfg._config}')