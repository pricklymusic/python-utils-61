import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults.copy()

    def load(self, path: str) -> 'ConfigLoader':
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    self._data.update(json.load(f))
            except (json.JSONDecodeError, IOError):
                pass
        return self

    def __getattr__(self, name: str) -> Any:
        if name not in self._data:
            raise AttributeError(f'Config key {name} missing')
        return self._data[name]

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def env_override(self, prefix: str = 'APP_') -> 'ConfigLoader':
        for key in self._data.keys():
            env_key = f'{prefix}{key.upper()}'
            if env_key in os.environ:
                val = os.environ[env_key]
                try:
                    self._data[key] = json.loads(val)
                except json.JSONDecodeError:
                    self._data[key] = val
        return self

def load_configuration(defaults: Dict[str, Any], path: str = 'config.json') -> ConfigLoader:
    return ConfigLoader(defaults).load(path).env_override()