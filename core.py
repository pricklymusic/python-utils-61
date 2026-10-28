import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def load_from_json(self, path: str) -> 'ConfigLoader':
        if os.path.exists(path):
            with open(path, 'r') as f:
                file_data = json.load(f)
                self._data.update(file_data)
        return self

    def __repr__(self) -> str:
        return f"ConfigLoader({self._data})"

def load_config(path: str, defaults: Dict[str, Any]) -> ConfigLoader:
    return ConfigLoader(defaults).load_from_json(path)

if __name__ == '__main__':
    # usage example: dynamic attribute access for settings
    cfg = load_config('settings.json', {'host': 'localhost', 'port': 8080})
    print(f"current host: {cfg.host}")