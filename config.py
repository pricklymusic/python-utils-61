import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self.data = defaults

    def load_from_env(self, prefix: str = 'APP_'):
        for key in self.data:
            env_key = f"{prefix}{key.upper()}"
            if env_key in os.environ:
                self.data[key] = os.environ[env_key]
        return self

    def load_from_json(self, path: str):
        if os.path.exists(path):
            with open(path, 'r') as f:
                self.data.update(json.load(f))
        return self

    def __getitem__(self, key: str) -> Any:
        return self.data.get(key)

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name)

def get_config(defaults: Dict[str, Any], path: str = 'config.json') -> ConfigLoader:
    return ConfigLoader(defaults).load_from_json(path).load_from_env()