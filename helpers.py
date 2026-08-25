import json
import os
from typing import Any, Dict, Optional

def _parse_value(value: str) -> Any:
    if value.lower() == 'true':
        return True
    if value.lower() == 'false':
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value

def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result

class Config:
    def __init__(self, data: Dict[str, Any]):
        self._data = data
    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            raise AttributeError(name)
        if name in self._data:
            value = self._data[name]
            if isinstance(value, dict):
                return Config(value)
            return value
        raise AttributeError(f"'Config' object has no attribute '{name}'")
    def __getitem__(self, key: str) -> Any:
        if key in self._data:
            value = self._data[key]
            if isinstance(value, dict):
                return Config(value)
            return value
        raise KeyError(key)
    def to_dict(self) -> Dict[str, Any]:
        return self._data.copy()

def load_config(
    defaults: Dict[str, Any],
    config_file: Optional[str] = None,
    env_prefix: str = "CONFIG_"
) -> Config:
    config = defaults.copy()
    if config_file and os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            file_config = json.load(f)
            config = _deep_merge(config, file_config)
    env_config: Dict[str, Any] = {}
    for key, value in os.environ.items():
        if key.startswith(env_prefix):
            config_key = key[len(env_prefix):].lower()
            parts = config_key.split('__')
            current = env_config
            for part in parts[:-1]:
                if part not in current or not isinstance(current.get(part), dict):
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = _parse_value(value)
    config = _deep_merge(config, env_config)
    return Config(config)