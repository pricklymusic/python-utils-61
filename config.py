import json
import os
from copy import deepcopy
from typing import Any, Dict, Optional

class ConfigLoadError(Exception):
    pass

def merge_configs(base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    result = deepcopy(base)
    to_process = [(result, updates)]
    while to_process:
        curr_base, curr_update = to_process.pop(0)
        for k, v in curr_update.items():
            if k in curr_base and isinstance(curr_base[k], dict) and isinstance(v, dict):
                to_process.append((curr_base[k], v))
            else:
                curr_base[k] = deepcopy(v)
    return result

class ConfigLoader:
    def __init__(self, defaults: Optional[Dict[str, Any]] = None) -> None:
        self.defaults = deepcopy(defaults) if defaults else {}
        self.config: Dict[str, Any] = deepcopy(self.defaults)

    def load_from_file(self, filepath: str) -> None:
        if not os.path.isfile(filepath):
            return
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.config = merge_configs(self.defaults, data)
        except (json.JSONDecodeError, IOError) as err:
            raise ConfigLoadError(f"Failed to load {filepath}: {err}") from err

    def load_from_dict(self, data: Dict[str, Any]) -> None:
        self.config = merge_configs(self.defaults, data)

    def apply_env_overrides(self, prefix: str = "APP_") -> None:
        for env_key, env_val in os.environ.items():
            if env_key.startswith(prefix):
                key_path = env_key[len(prefix):].lower().split('__')
                current = self.config
                for part in key_path[:-1]:
                    if part not in current or not isinstance(current[part], dict):
                        current[part] = {}
                    current = current[part]
                current[key_path[-1]] = env_val

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        current = self.config
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        return current

    def __getitem__(self, key: str) -> Any:
        if key in self.config:
            return self.config[key]
        raise KeyError(key)

    def as_dict(self) -> Dict[str, Any]:
        return deepcopy(self.config)

    def reset_to_defaults(self) -> None:
        self.config = deepcopy(self.defaults)

def create_loader(defaults: Dict[str, Any], file: Optional[str] = None) -> ConfigLoader:
    loader = ConfigLoader(defaults)
    if file:
        loader.load_from_file(file)
    loader.apply_env_overrides()
    return loader