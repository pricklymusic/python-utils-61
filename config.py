import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self.config = defaults

    def __getitem__(self, key: str) -> Any:
        return self.config.get(key)

    def load_from_env(self, prefix: str = 'APP_') -> None:
        for key in self.config:
            env_val = os.getenv(f"{prefix}{key.upper()}")
            if env_val is not None:
                try:
                    self.config[key] = json.loads(env_val)
                except (json.JSONDecodeError, TypeError):
                    self.config[key] = env_val

    def load_from_json(self, filepath: str) -> None:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self.config.update(json.load(f))

    def __repr__(self) -> str:
        return str(self.config)

def create_config(defaults: Dict[str, Any]) -> ConfigLoader:
    instance = ConfigLoader(defaults)
    return instance

if __name__ == '__main__':
    cfg = create_config({'host': 'localhost', 'port': 8080, 'debug': False})
    cfg.load_from_env()
    print(f"Active configuration: {cfg}")