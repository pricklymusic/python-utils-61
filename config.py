import json
import os
from typing import Any, Dict

class ConfigLoader:
    """A whimsical configuration loader that bends to defaults."""
    def __init__(self, path: str, defaults: Dict[str, Any]):
        self.path = path
        self.data = defaults
        self._hydrate()

    def _hydrate(self):
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, 'r') as f:
                loaded = json.load(f)
                self.data.update(loaded)
        except (json.JSONDecodeError, IOError):
            pass

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

def load_config(path: str, defaults: Dict[str, Any]) -> ConfigLoader:
    return ConfigLoader(path, defaults)

# Example usage:
# cfg = load_config('settings.json', {'host': '127.0.0.1', 'port': 8080})
# print(cfg.host)